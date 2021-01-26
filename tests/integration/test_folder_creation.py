import unittest
import uuid
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth


class TestFolderCreation(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.auth.login()
        self.api = Api(self.auth)

        self.random_folder_name = uuid.uuid1()

    def tearDown(self) -> None:
        self.api.delete_file(self.random_folder_name)

    def test_when_send_folder_creation_request_then_returns_ok_response(self):
        response = self.api.create_user_sub_folder(self.random_folder_name)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)

    def test_when_send_folder_structure_creation_request_then_returns_ok_response(self):
        folder1 = str(uuid.uuid1())
        folder2 = str(uuid.uuid1())
        self.random_folder_name = '/'.join([folder1, folder2])
        expected_user_files_response = [
            {
                "name": folder2,
                "path": "user/{}".format(folder1),
                "size": 4096,
                "type": "DIR"
            }
        ]

        folder_creation_response = self.api.create_user_sub_folder(self.random_folder_name)

        self.assertEqual(folder_creation_response.status, HTTPStatus.OK)
        self.assertFalse(folder_creation_response.json)

        folder_query_response = self.api.get_user_files(folder1)

        self.assertEqual(folder_query_response.status, HTTPStatus.OK)
        self.assertEqual(len(folder_query_response.json), 1)
        self.assertEqual(folder_query_response.json, expected_user_files_response)

        self.api.delete_file(folder1)


if __name__ == '__main__':
    unittest.main()
