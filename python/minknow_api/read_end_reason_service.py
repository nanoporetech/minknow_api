### THIS FILE IS AUTOGENERATED. DO NOT EDIT THIS FILE DIRECTLY ###
import minknow_api
from minknow_api.read_end_reason_pb2_grpc import *
import minknow_api.read_end_reason_pb2 as read_end_reason_pb2
from minknow_api.read_end_reason_pb2 import *
from minknow_api._support import MessageWrapper, ArgumentError
import time
import logging
import sys

__all__ = [
    "ReadEndReason",
    "All",
    "Unknown",
    "Partial",
    "MuxChange",
    "UnblockMuxChange",
    "SignalPositive",
    "SignalNegative",
    "DataServiceUnblockMuxChange",
    "AnalysisConfigChange",
]

def run_with_retry(method, message, timeout, unwraps, full_name):
    retry_count = 20
    error = None
    for i in range(retry_count):
        try:
            result = MessageWrapper(method(message, timeout=timeout), unwraps=unwraps)
            return result
        except grpc.RpcError as e:
            # Retrying unidentified grpc errors to keep clients from crashing
            retryable_error = (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details() or \
                                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()))
            if retryable_error:
                logging.info('Bypassed ({}: {}) error for grpc: {}. Attempt {}.'.format(e.code(), e.details(), full_name, i))
            else:
                raise
            error = e
        time.sleep(1)
    raise error


