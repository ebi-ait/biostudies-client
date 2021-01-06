import unittest
from http import HTTPStatus
from unittest.mock import Mock

from requests import Response

from biostudiesclient.response_utils import ResponseUtils


class TestResponseUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.response_utils = ResponseUtils()
        self.valid_session_id = "123.456.789"

    def test_when_processing_ok_response_return_response_object_without_error(self):
        input_response = Mock(spec=Response)
        input_response.status_code = HTTPStatus.OK
        response_text = self.correct_response_text_with_session_id()
        input_response.json.return_value = response_text

        output_response = self.response_utils.handle_response(input_response)

        self.assertEqual(output_response.status, HTTPStatus.OK)
        self.assertEqual(output_response.json, response_text)

    def correct_response_text_with_session_id(self):
        return {
            "sessid": self.valid_session_id,
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


if __name__ == '__main__':
    unittest.main()
