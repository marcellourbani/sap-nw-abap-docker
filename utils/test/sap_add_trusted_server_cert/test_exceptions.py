import unittest
import setup


setup.init()
sap_add_trusted_server_cert = setup.import_utils_executable('sap_add_trusted_server_cert')


class TestUploadException(unittest.TestCase):

    def test_ctor_with_message(self):
        ex = sap_add_trusted_server_cert.UploadCertError('Something has failed')
        self.assertEqual(ex.message, 'Something has failed')


class TestInvalidSSLStorage(unittest.TestCase):

    def test_ctor_with_message(self):
        ex = sap_add_trusted_server_cert.InvalidSSLStorage('Something has failed')
        self.assertEqual(ex.message, 'Something has failed')


class TestPutCertificateError(unittest.TestCase):

    def test_ctor_with_message(self):
        ex = sap_add_trusted_server_cert.PutCertificateError('Something has failed')
        self.assertEqual(ex.message, 'Something has failed')


if __name__ == '__main__':
    unittest.main()
