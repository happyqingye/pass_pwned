# import unittest
# from unittest import mock
# import requests
# from models import PassEncrypt, HIBPApi
#
#
# __author__ = 'sehlat57'
#
#
# class TestPassEncryptTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.encryption = PassEncrypt('P@ssworD').encrypt()
#
#     def test_encrypt(self):
#         self.assertEqual(self.encryption,
#                          '8cb0ada553171368e4daf7d332789eb4c5e15ad4')
#
#
# class TestPasswdCheckTestCase(unittest.TestCase):
#
#     @mock.patch('models.requests')
#     def test_passwd_check_200(self, mock_requests):
#         mock_requests.post.return_value = mock.Mock(status_code=200)
#
#         passwd_test = HIBPApi(passwd='P@ssworD', file_passwd=None)
#         self.assertEqual('\x1b[1;31mYour password is PWNeD :(\x1b[0m',
#                          passwd_test.passwd_check())
#
#     @mock.patch('models.requests')
#     def test_passwd_check_404(self, mock_requests):
#         mock_requests.post.return_value = mock.Mock(status_code=404)
#
#         passwd_test = HIBPApi(passwd='P@ssworD', file_passwd=None)
#         self.assertEqual('\x1b[1;32mYour password not found in HIBP DB\x1b[0m',
#                          passwd_test.passwd_check())
#
#     @mock.patch('models.requests')
#     def test_passwd_check_exception(self, mock_requests):
#         http_error = requests.exceptions.ConnectionError
#         mock_requests.raiseError.side_effect = http_error
#         passwd_test = HIBPApi(passwd='P@ssworD', file_passwd=None)
#         self.assertIs(None, passwd_test.passwd_check())
#
# if __name__ == "__main__":
#     unittest.main()
#
#
#
#
#ToDO update tests to new api