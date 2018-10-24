import backports.unittest_mock
backports.unittest_mock.install()

import unittest
from unittest import mock

import setup

setup.init()

# replaced by a mock in setup.init()
import pyrfc

sap_add_trusted_server_cert = setup.import_utils_executable('sap_add_trusted_server_cert')

SSLCertStorage = sap_add_trusted_server_cert.SSLCertStorage
InvalidSSLStorage = sap_add_trusted_server_cert.InvalidSSLStorage
PutCertificateError = sap_add_trusted_server_cert.PutCertificateError


class TestSSLCertStoraget(unittest.TestCase):

    def test_ctor(self):
        conn = pyrfc.Connection()

        ssl_storage = SSLCertStorage(conn, 'CTXT', 'APPL')

        self.assertIs(ssl_storage._conn, conn)
        self.assertEqual(ssl_storage.identity['PSE_CONTEXT'], 'CTXT')
        self.assertEqual(ssl_storage.identity['PSE_APPLIC'], 'APPL')

    def test_client_anonymous_storage(self):
        conn = pyrfc.Connection()

        anon_ssl_storage = SSLCertStorage.client_anonymous_storage(conn)

        self.assertIs(anon_ssl_storage._conn, conn)
        self.assertEqual(anon_ssl_storage.identity['PSE_CONTEXT'], 'SSLC')
        self.assertEqual(anon_ssl_storage.identity['PSE_APPLIC'], 'ANONYM')

    def test_repr(self):
        conn = pyrfc.Connection()

        ssl_storage = SSLCertStorage(conn, 'REPR', 'TEST')
        self.assertEquals(repr(ssl_storage), 'SSL Storage REPR/TEST')

    def test_str(self):
        conn = pyrfc.Connection()

        ssl_storage = SSLCertStorage(conn, 'STR', 'TEST')
        self.assertEquals(str(ssl_storage), 'SSL Storage STR/TEST')

    @unittest.mock.patch('pyrfc.Connection')
    def test_raise_if_not_ok_raises(self, mock_connection):
        mock_connection.call.return_value = {
            'ET_BAPIRET2': [{'TYPE': 'E', 'MESSAGE': 'Invalid storage'}]}

        ssl_storage = SSLCertStorage(mock_connection, 'RAISE', 'TEST')

        with self.assertRaises(sap_add_trusted_server_cert.InvalidSSLStorage) as cm:
            ssl_storage.raise_if_not_ok()

        self.assertEquals(mock_connection.call.call_args_list,
                          [mock.call('SSFR_PSE_CHECK',
                                     IS_STRUST_IDENTITY={'PSE_CONTEXT': 'RAISE',
                                                         'PSE_APPLIC': 'TEST'})])

        self.assertEquals(str(cm.exception),
                          'The SSL Storage RAISE/TEST is broken: Invalid storage')

    @unittest.mock.patch('pyrfc.Connection')
    def test_raise_if_not_ok(self, mock_connection):
        mock_connection.call.return_value = {'ET_BAPIRET2': [{'TYPE': 'S'}]}

        ssl_storage = SSLCertStorage(mock_connection, 'NOTRAISE', 'TEST')
        ssl_storage.raise_if_not_ok()

        self.assertEquals(mock_connection.call.call_args_list,
                          [mock.call('SSFR_PSE_CHECK',
                                     IS_STRUST_IDENTITY={'PSE_CONTEXT': 'NOTRAISE',
                                                         'PSE_APPLIC': 'TEST'})])

    @unittest.mock.patch('pyrfc.Connection')
    def test_put_certificate(self, mock_connection):
        mock_connection.call.return_value = {'ET_BAPIRET2': []}

        ssl_storage = SSLCertStorage(mock_connection, 'PUTOK', 'TEST')

        ssl_storage.put_certificate('plain old data')

        self.assertEquals(mock_connection.call.call_args_list,
                          [mock.call('SSFR_PUT_CERTIFICATE',
                                     IS_STRUST_IDENTITY={'PSE_CONTEXT': 'PUTOK',
                                                         'PSE_APPLIC': 'TEST'},
                                     IV_CERTIFICATE=u'plain old data')])

    @unittest.mock.patch('pyrfc.Connection')
    def test_put_certificate_fail(self, mock_connection):
        mock_connection.call.return_value = {
            'ET_BAPIRET2': [{'TYPE': 'E', 'MESSAGE': 'Put has failed'}]}

        ssl_storage = SSLCertStorage(mock_connection, 'PUTERR', 'TEST')

        with self.assertRaises(sap_add_trusted_server_cert.PutCertificateError) as cm:
            ssl_storage.put_certificate('plain old data')

        self.assertEquals(mock_connection.call.call_args_list,
                          [mock.call('SSFR_PUT_CERTIFICATE',
                                     IS_STRUST_IDENTITY={'PSE_CONTEXT': 'PUTERR',
                                                         'PSE_APPLIC': 'TEST'},
                                     IV_CERTIFICATE=u'plain old data')])

        self.assertEquals(str(cm.exception),
                          'Failed to put the CERT to the SSL Storage PUTERR/TEST: '
                          'Put has failed')


if __name__ == '__main__':
    unittest.main()
