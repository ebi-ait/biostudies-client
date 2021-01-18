import os
import unittest
from http import HTTPStatus

from biostudiesclient.auth import Auth
from biostudiesclient.exceptions import RestErrorException

INVALID_CREDENTIALS_MESSAGE = "Invalid email address or password."


class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()

    def test_when_login_with_correct_credentials_then_returns_correct_response(self):
        response = self.auth.login()

        self.assertTrue(response.session_id)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.error_message)

    def test_when_login_with_wrong_credentials_from_env_then_raises_exception(self):
        existing_username_from_env = os.environ['BIOSTUDIES_USERNAME']
        existing_password_from_env = os.environ['BIOSTUDIES_PASSWORD']

        os.environ['BIOSTUDIES_USERNAME'] = "non_existing_user"
        os.environ['BIOSTUDIES_PASSWORD'] = "wrong_password"

        with self.assertRaises(RestErrorException) as context:
            self.auth.login()

        self.assertTrue(INVALID_CREDENTIALS_MESSAGE in context.exception.message)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, context.exception.status_code)

        os.environ['BIOSTUDIES_USERNAME'] = existing_username_from_env
        os.environ['BIOSTUDIES_PASSWORD'] = existing_password_from_env

    def test_when_login_with_invalid_credentials_then_raises_exception(self):
        username = "non_existing_user"
        password = "wrong_password"

        with self.assertRaises(RestErrorException) as context:
            self.auth.login(username, password)

        self.assertTrue(INVALID_CREDENTIALS_MESSAGE in context.exception.message)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, context.exception.status_code)


if __name__ == '__main__':
    unittest.main()
