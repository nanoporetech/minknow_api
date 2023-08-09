import logging
import unittest

import minknow_api
from minknow_api.testutils import MockMinKNOWServer

LOGGER = logging.getLogger(__name__)


class TestMockServer(unittest.TestCase):
    def setUp(self):
        self.test_server = MockMinKNOWServer()
        self.test_server.start()

        ssl_creds = self.test_server.make_channel_credentials()
        self.connection = minknow_api.Connection(
            self.test_server.port, credentials=ssl_creds
        )
        LOGGER.info("Connected on {}".format(self.test_server.port))

    def tearDown(self):
        self.test_server.stop(0)

    def test_get_version_info(self):
        """Get the version info

        This is an example of a simple RPC
        """
        version_info = self.connection.instance.get_version_info()
        self.assertEqual(minknow_api.__version__, version_info.minknow.full)


if __name__ == "__main__":
    unittest.main()
