import backports.unittest_mock
backports.unittest_mock.install()

import unittest
from unittest import mock

import setup

setup.init()

# replaced by a mock in setup.init()
import pyrfc

sap_add_trusted_server_cert = setup.import_utils_executable('sap_add_trusted_server_cert')

SecretValue = sap_add_trusted_server_cert.SecretValue

class TestArgumentParser(unittest.TestCase):

    @mock.patch('sap_add_trusted_server_cert.add_trusted_server_certs')
    def test_default(self, mock_fn):
         sap_add_trusted_server_cert._main(['/path/1', '/path/2'])

         conn_spec = sap_add_trusted_server_cert.ConnectionDetails(
            ashost='localhost', sysnr='00', client='001',
            user=SecretValue('DEVELOPER'), passwd=SecretValue('Down1oad'),
            sid='NPL')
         self.assertEquals(mock_fn.call_args_list, [mock.call(conn_spec, ['/path/1', '/path/2'])])


if __name__ == '__main__':
    unittest.main()
