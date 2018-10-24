import unittest
import setup


setup.init()
sap_add_trusted_server_cert = setup.import_utils_executable('sap_add_trusted_server_cert')

SecretValue = sap_add_trusted_server_cert.SecretValue


class TestConnectionDetails(unittest.TestCase):

    def test_ctor(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'))

        self.assertEqual(connDetails._params['ashost'], 'sap.example.org')
        self.assertEqual(connDetails._params['sysnr'], '99')
        self.assertEqual(connDetails._params['client'], '666')
        self.assertNotIn('sid', connDetails._params)
        self.assertEqual(connDetails._user.decode(), 'ANGEL')
        self.assertEqual(connDetails._passwd.decode(), 'Victory')

    def test_ctor_with_sid(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'),
                sid='XYZ')

        self.assertEqual(connDetails._params['ashost'], 'sap.example.org')
        self.assertEqual(connDetails._params['sysnr'], '99')
        self.assertEqual(connDetails._params['client'], '666')
        self.assertEqual(connDetails._params['sid'], 'XYZ')
        self.assertEqual(connDetails._user.decode(), 'ANGEL')
        self.assertEqual(connDetails._passwd.decode(), 'Victory')

    def test_str(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'))

        self.assertEqual('ANGEL in sap.example.org/666', str(connDetails))

    def test_str_with_sid(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'),
                sid='XYZ')

        self.assertEqual('ANGEL in XYZ/666', str(connDetails))

    def test_repr(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'))

        self.assertEqual('ANGEL in sap.example.org/666', repr(connDetails))

    def test_repr_with_sid(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'),
                sid='XYZ')

        self.assertEqual('ANGEL in XYZ/666', repr(connDetails))

    def test_eq_self(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'sap.example.org', '99', '666',
                SecretValue('ANGEL'), SecretValue('Victory'),
                sid='XYZ')

        self.assertEqual(connDetails, connDetails)

    def test_to_params(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'host.example.org', '69', '777',
                SecretValue('DEVELOPER'), SecretValue('SUCCESS'))

        kwparams = connDetails.to_params()

        self.assertEqual(kwparams['ashost'], 'host.example.org')
        self.assertEqual(kwparams['sysnr'], '69')
        self.assertEqual(kwparams['client'], '777')
        self.assertEqual(kwparams['user'], 'DEVELOPER')
        self.assertEqual(kwparams['passwd'], 'SUCCESS')

    def test_to_params_returns_copy(self):
        connDetails = sap_add_trusted_server_cert.ConnectionDetails(
                'host.example.org', '69', '777',
                SecretValue('DEVELOPER'), SecretValue('SUCCESS'))

        kwparams = connDetails.to_params()

        self.assertEqual(kwparams['ashost'], 'host.example.org')

        kwparams['ashost'] = 'host.example.org'

        kkwparams = connDetails.to_params()

        self.assertEqual(kwparams['ashost'], 'host.example.org')


if __name__ == '__main__':
    unittest.main()
