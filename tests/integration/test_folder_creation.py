import unittest
import uuid
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth
from tests.test_utils import TestUtils


class TestFolderCreation(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.session_id = TestUtils.get_session_id(auth=self.auth)
        self.api = Api(session_id=self.session_id)

        self.random_folder_name = uuid.uuid1()

    def tearDown(self) -> None:
        self.api.delete_file(self.random_folder_name)

    def test_when_send_folder_creation_request_then_returns_ok_response(self):
        response = self.api.create_user_sub_folder(self.random_folder_name)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)


if __name__ == '__main__':
    unittest.main()
