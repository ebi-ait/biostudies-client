import unittest
from http import HTTPStatus

from mock import patch

from biostudiesclient.api import Api
from biostudiesclient.response_utils import TRY_IT_AGAIN_LATER_MESSAGE, WRONG_REQUEST_URL_MESSAGE


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        self.api = Api()

    @patch('biostudiesclient.api.requests.post')
    def test_when_request_wrong_url_then_returns_not_found_response(self, mock_post):
        url = 'http://example.com/wrong/path'
        folder_name = "test_folder"
        session_id = 'test.session.id'

        mock_post.return_value.status_code = HTTPStatus.NOT_FOUND
        mock_post.return_value.url = url

        response = self.api.create_user_sub_folder(session_id, folder_name)

        self.assertEqual(response.status, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.error_message, WRONG_REQUEST_URL_MESSAGE.format(URL=url))

    @patch('biostudiesclient.api.requests.post')
    def test_when_passing_folder_name_then_folder_created(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.OK

        folder_name = "test_folder"
        session_id = 'test.session.id'

        response = self.api.create_user_sub_folder(session_id, folder_name)

        self.assertEqual(response.status, HTTPStatus.OK)

    @patch('biostudiesclient.api.requests.post')
    def test_when_passing_incorrect_session_id_then_response_with_error(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        folder_name = "test_folder"
        session_id = 'incorrect.session.id'

        response = self.api.create_user_sub_folder(session_id, folder_name)

        self.assertEqual(response.status, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.error_message, TRY_IT_AGAIN_LATER_MESSAGE)

    @patch('biostudiesclient.api.requests.post')
    def test_when_upload_a_file_then_returns_ok_response(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.OK

        file_path = "resources/test_file.txt"
        session_id = 'test.session.id'

        response = self.api.upload_file(session_id, file_path)

        self.assertEqual(response.status, HTTPStatus.OK)

    @patch('biostudiesclient.api.requests.post')
    def test_when_upload_a_file_with_wrong_header_then_returns_error_response(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.BAD_REQUEST

        file_path = "resources/test_file.txt"
        session_id = 'test.session.id'

        response = self.api.upload_file(session_id, file_path)

        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
