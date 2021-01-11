import unittest
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth


class TestFileUpload(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.session_id = self.__get_session_id()
        self.api = Api(session_id=self.session_id)

    def test_when_upload_a_file_then_returns_ok_response(self):
        file_path = "tests/resources/test_file.txt"

        response = self.api.upload_file(file_path)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)
        self.assertFalse(response.error_message)

    def __get_session_id(self):
        auth_response = self.auth.login()
        auth_status = auth_response.status

        if auth_status == HTTPStatus.OK:
            return auth_response.session_id
        else:
            return auth_response.error_message


if __name__ == '__main__':
    unittest.main()
