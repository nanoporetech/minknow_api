"""test_bidirectional_rpc.py

This test case considers RPCs that stream requests
and responses between the gPRC client and server.

As a test case we are using the ``get_live_reads``
function from the data service. This RPC works by:

# TODO: Explanation of data flow in this RPC
"""
import logging
import random
import time
import unittest
from queue import Empty, Queue
from threading import Thread
from uuid import uuid4

import numpy as np

import minknow_api
from minknow_api.testutils import MockMinKNOWServer


class DataServicer(minknow_api.data_pb2_grpc.DataServiceServicer):
    def __init__(self):
        self.setup = False
        self.first = None
        self.last = None
        self.dtype = None
        self.action_responses = []
        self.processed_requests = 0
        self.logger = logging.getLogger("[SERVER]")

    def _read_data_generator(self):
        """Generate a (channel, ReadData) tuple, using random numbers"""
        for channel in range(self.first, self.last + 1):
            # 40% chance of skipping a read, simulates sparse read data
            if np.random.choice([True, False], 1, p=[0.4, 0.6]):
                continue
            sample_length = random.randint(1000, 3000)
            sample_number = 0
            defaults = dict(
                id=str(uuid4()),
                number=random.randint(1, 10000),
                start_sample=sample_number,
                chunk_start_sample=sample_number,
                chunk_length=sample_length,
                chunk_classifications=[83],
                raw_data=np.random.randint(
                    20, 450, sample_length, dtype=np.int16
                ).tobytes(),
                median_before=random.uniform(
                    200, 250
                ),  # guarantee > 60 pa delta - simple treats this as a read.
                median=random.uniform(100, 120),
            )

            yield channel, minknow_api.data_pb2.GetLiveReadsResponse.ReadData(
                **defaults
            )

    def request_handler(self, iterator):
        for req in iterator:
            if req.HasField("setup"):
                self.logger.info("Received StreamSetup request")
                self.setup = True
                self.first = req.setup.first_channel
                self.last = req.setup.last_channel
                self.dtype = req.setup.raw_data_type
            elif not self.setup:
                raise RuntimeError("Expected StreamSetup first")
            elif req.HasField("actions"):
                for resp in req.actions.actions:
                    self.processed_requests += 1
                    self.action_responses.append(
                        minknow_api.data_pb2.GetLiveReadsResponse.ActionResponse(
                            action_id=resp.action_id,
                            response=minknow_api.data_pb2.GetLiveReadsResponse.ActionResponse.Response.SUCCESS,
                        )
                    )
            else:
                raise RuntimeError("Uhh oh")

    def get_live_reads(self, request_iterator, context):

        request_thread = Thread(target=self.request_handler, args=(request_iterator,))
        request_thread.start()
        while request_thread.is_alive():
            if not self.setup:
                continue
            yield minknow_api.data_pb2.GetLiveReadsResponse(
                samples_since_start=0,
                seconds_since_start=0,
                # map<int32, ReadData> (channel, ReadData)
                channels={
                    channel: read_data
                    for channel, read_data in self._read_data_generator()
                },
                # repeated ActionResponse
                action_responses=self.action_responses,
            )
            self.action_responses = []
            time.sleep(1)


def request_generator(logger, action_queue, return_queue):
    """Iterable that sends messages to the server

    First request is StreamSetup, following requests
    are Actions
    """
    logger.info("Sending StreamSetup")
    yield minknow_api.data_pb2.GetLiveReadsRequest(
        setup=minknow_api.data_pb2.GetLiveReadsRequest.StreamSetup(
            first_channel=1,
            last_channel=512,
            raw_data_type=minknow_api.data_pb2.GetLiveReadsRequest.RawDataType.CALIBRATED,
            sample_minimum_chunk_size=0,
        )
    )
    sent_actions = 0
    action_batch_size = 512
    t_end = time.time() + 30
    while time.time() <= t_end:
        actions = []
        for _ in range(action_batch_size):
            try:
                action = action_queue.get_nowait()
            except Empty:
                break
            else:
                actions.append(action)

        if actions:
            yield minknow_api.data_pb2.GetLiveReadsRequest(
                actions=minknow_api.data_pb2.GetLiveReadsRequest.Actions(
                    actions=actions
                )
            )
            sent_actions += len(actions)
    else:
        return_queue.put(sent_actions)


class TestBidirectionalRPC(unittest.TestCase):
    def setUp(self) -> None:
        # Here we initialise the server
        self.server = MockMinKNOWServer(data_service=DataServicer)
        self.port = self.server.port
        self.server.start()

        ssl_creds = self.server.make_channel_credentials()
        self.connection = minknow_api.Connection(self.port, credentials=ssl_creds)

    def tearDown(self) -> None:
        self.server.stop(0)
        pass

    def test_get_live_reads(self):
        logger = logging.getLogger("[CLIENT]")
        action_queue = Queue()
        return_queue = Queue()
        action_responses = 0
        response_gen = request_generator(logger, action_queue, return_queue)
        response_stream = self.connection.data.get_live_reads(response_gen)
        for resp in response_stream:
            for action_response in resp.action_responses:
                action_responses += 1

            for key in resp.channels:
                r = resp.channels[key]
                action_queue.put(
                    minknow_api.data_pb2.GetLiveReadsRequest.Action(
                        action_id=str(uuid4()),
                        channel=key,
                        number=r.number,
                        unblock=minknow_api.data_pb2.GetLiveReadsRequest.UnblockAction(
                            duration=1,
                        ),
                    )
                )

        sent_actions = return_queue.get()
        logger.info(
            "{} {}".format(
                sent_actions,
                self.server.data_service.processed_requests,
            )
        )
        self.assertEqual(sent_actions, self.server.data_service.processed_requests)


if __name__ == "__main__":
    unittest.main()
