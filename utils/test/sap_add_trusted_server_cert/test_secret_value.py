import unittest
import setup


setup.init()
sap_add_trusted_server_cert = setup.import_utils_executable('sap_add_trusted_server_cert')


class TestSecretValue(unittest.TestCase):

    def test_stores_encoded(self):
        storage = sap_add_trusted_server_cert.SecretValue('foo')
        self.assertNotEqual('foo', storage._value)
        self.assertEqual(storage._value.lower().find('foo'), -1)

    def test_can_decode(self):
        storage = sap_add_trusted_server_cert.SecretValue('bar')
        self.assertEqual(storage.decode(), 'bar')


if __name__ == '__main__':
    unittest.main()
