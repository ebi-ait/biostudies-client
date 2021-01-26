import os
import unittest
import uuid
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth


class TestFileUpload(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.auth.login()
        self.api = Api(self.auth)

        self.file_path = "tests/resources/test_file.txt"

    def tearDown(self) -> None:
        self.api.delete_file(os.path.basename(self.file_path))

    def test_when_upload_a_file_then_returns_ok_response(self):
        response = self.api.upload_file(self.file_path)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)

    def test_when_upload_a_file_to_an_existing_sub_folder_then_returns_ok_response(self):
        folder1 = str(uuid.uuid1())
        folder2 = str(uuid.uuid1())
        random_folder_name = '/'.join([folder1, folder2])

        folder_creation_response = self.api.create_user_sub_folder(random_folder_name)

        self.assertEqual(folder_creation_response.status, HTTPStatus.OK)
        self.assertFalse(folder_creation_response.json)

        file_upload_response = self.api.upload_file(self.file_path, random_folder_name)

        self.assertEqual(file_upload_response.status, HTTPStatus.OK)
        self.assertFalse(file_upload_response.json)

        self.api.delete_file(folder1)


if __name__ == '__main__':
    unittest.main()
