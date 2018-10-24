import backports.unittest_mock
backports.unittest_mock.install()

import unittest
from unittest import mock
from unittest.mock import patch, mock_open, call

import setup

setup.init()

# replaced by a mock in setup.init()
import pyrfc

sap_add_trusted_server_cert = setup.import_utils_executable('sap_add_trusted_server_cert')
SecretValue = sap_add_trusted_server_cert.SecretValue

class TestAddAllFiles(unittest.TestCase):

    @mock.patch('sap_add_trusted_server_cert.Connection')
    def test_smooth_run(self, mock_connection):
        def rfc_response(function, **kwargs):
            return {'SSFR_PSE_CHECK': {'ET_BAPIRET2': [{'TYPE': 'S'}]},
                    'SSFR_PUT_CERTIFICATE': {'ET_BAPIRET2': []}}[function]

        instance = mock.Mock()
        instance.call = mock.Mock(side_effect=rfc_response)
        instance.__enter__ = mock.Mock(return_value=instance)
        instance.__exit__ = mock.Mock(return_value=False)

        mock_connection.return_value = instance

        conn_spec = sap_add_trusted_server_cert.ConnectionDetails(
            ashost='localhost', sysnr='00', client='001',
            user=SecretValue('DEVELOPER'), passwd=SecretValue('Down1oad'),
            sid='NPL')

        with patch('sap_add_trusted_server_cert.open', mock_open(read_data='CERT')) as mock_file:
            sap_add_trusted_server_cert.add_trusted_server_certs(
                conn_spec, ['/path/1', '/path/2'])

        self.assertEquals(
            mock_file.mock_calls,
            [call('/path/1'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None),
            call('/path/2'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None)])

        self.assertEquals(
            instance.call.call_args_list,
            [call('SSFR_PSE_CHECK',
                  IS_STRUST_IDENTITY={'PSE_CONTEXT': u'SSLC', 'PSE_APPLIC': u'ANONYM'}),
             call('SSFR_PUT_CERTIFICATE',
                  IS_STRUST_IDENTITY={'PSE_CONTEXT': u'SSLC', 'PSE_APPLIC': u'ANONYM'},
                  IV_CERTIFICATE='CERT'),
             call('SSFR_PUT_CERTIFICATE',
                 IS_STRUST_IDENTITY={'PSE_CONTEXT': u'SSLC', 'PSE_APPLIC': u'ANONYM'},
                 IV_CERTIFICATE='CERT')])


if __name__ == '__main__':
    unittest.main()
