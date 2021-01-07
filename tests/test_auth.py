import unittest
from http import HTTPStatus

from mock import patch
from biostudiesclient.auth import Auth


class TestAuth(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.biostudies_username = 'username'
        self.biostudies_password = 'pwd'
        self.valid_sessid = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJpZFwiOjExLFwiZW1haWxcIjpcImthcm9seUBlYmkuYWMudWtcIixcImZ1bGxOYW1lXCI6XCJVbmlmaWVkIFN1Ym1pc3Npb24gSW50ZXJmYWNlXCIsXCJjcmVhdGlvblRpbWVcIjoxNjA4MjI0MjM5fSJ9.wxJ4cIbKfGzRxukDDblYXqLLUI1mZF7iS5A9xupj2dMaVgUaXhgNJEqMdRA2ouhS1LaZoIgH8Ri6Xssj0AzSqw"
        self.auth_error_message = "Invalid email address or password."
        self.valid_auth_response = {
            "sessid": self.valid_sessid,
            "email": "test@email.uk",
            "username": "test_username",
            "secret": "aa/aabbcc-1122-4785-a875-cfade60fbb7c-a11",
            "fullname": "Test Full Name",
            "superuser": False,
            "allow": [
                "Public"
            ],
            "deny": [],
            "aux": {
                "orcid": ""
            }
        }
        self.invalid_auth_response = {
            "status": "FAIL",
            "log": {
                "level": "ERROR",
                "message": self.auth_error_message,
                "subnodes": []
            }
        }

    @patch('biostudiesclient.auth.requests.post')
    def test_given_correct_credentials_can_login(self, mock_post):
        mock_post.return_value.json.return_value = self.valid_auth_response
        mock_post.return_value.status_code = HTTPStatus.OK

        response = self.auth.login()

        self.assertEqual(response.session_id, self.valid_sessid)
        self.assertEqual(response.status, HTTPStatus.OK)

    @patch('biostudiesclient.auth.requests.post')
    def test_given_incorrect_credentials_returns_error(self, mock_post):
        mock_post.return_value.json.return_value = self.invalid_auth_response
        mock_post.return_value.status_code = HTTPStatus.UNAUTHORIZED

        response = self.auth.login()

        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)
        self.assertTrue(response.session_id == "")
        self.assertEqual(response.error_message, self.auth_error_message)


if __name__ == '__main__':
    unittest.main()
