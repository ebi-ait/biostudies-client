import unittest
from http import HTTPStatus

from biostudiesclient.auth import Auth

INVALID_CREDENTIALS_MESSAGE = "Invalid email address or password."


class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()

    def test_when_login_with_correct_credentials_then_returns_correct_response(self):
        response = self.auth.login()

        self.assertTrue(response.session_id)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.error_message)

    def test_when_login_with_invalid_credentials_then_returns_error_response(self):
        self.auth.username = "non_existing_user"
        self.auth.password = "wrong_password"

        response = self.auth.login()

        self.assertFalse(response.session_id)
        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)
        self.assertTrue(response.error_message)
        self.assertEqual(response.error_message, INVALID_CREDENTIALS_MESSAGE)


if __name__ == '__main__':
    unittest.main()
