import os
import unittest
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth
from tests.test_utils import TestUtils


class TestFileUpload(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.session_id = TestUtils.get_session_id(auth=self.auth)
        self.api = Api(session_id=self.session_id)

        self.file_path = "tests/resources/test_file.txt"

    def tearDown(self) -> None:
        self.api.delete_file(os.path.basename(self.file_path))

    def test_when_upload_a_file_then_returns_ok_response(self):
        response = self.api.upload_file(self.file_path)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)
        self.assertFalse(response.error_message)


if __name__ == '__main__':
    unittest.main()
