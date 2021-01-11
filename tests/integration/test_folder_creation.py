import unittest
import uuid
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth


class TestFolderCreation(unittest.TestCase):
    def setUp(self) -> None:
        self.auth = Auth()
        self.session_id = self.__get_session_id()
        self.api = Api(session_id=self.session_id)

        self.random_folder_name = uuid.uuid1()

    def tearDown(self) -> None:
        self.api.delete_file(self.random_folder_name)

    def test_when_send_folder_creation_request_then_returns_ok_response(self):
        response = self.api.create_user_sub_folder(self.random_folder_name)

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
