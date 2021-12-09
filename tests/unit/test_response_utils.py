import json
import unittest
from http import HTTPStatus
from unittest.mock import Mock

from assertpy import assert_that
from requests import Response

from biostudiesclient.exceptions import RestErrorException
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
        input_response.text = response_text

        output_response = self.response_utils.handle_response(input_response)

        self.assertEqual(output_response.status, HTTPStatus.OK)
        self.assertEqual(output_response.json, response_text)

    def test_when_processing_plain_error_message_returns_parsed_message(self):
        input_response = Mock(spec=Response)
        input_response.status_code = HTTPStatus.REQUEST_TIMEOUT
        error_message: str = '{"message":"Something went wrong."}'
        input_response.json.return_value = json.loads(error_message)
        input_response.text = error_message

        assert_that(self.response_utils.handle_response)\
            .raises(RestErrorException)\
            .when_called_with(input_response)\
            .starts_with("('Something")\
            .is_equal_to("('Something went wrong.', <HTTPStatus.REQUEST_TIMEOUT: 408>)")

    def test_when_processing_detailed_error_message_returns_parsed_message(self):
        input_response = Mock(spec=Response)
        input_response.status_code = HTTPStatus.BAD_REQUEST
        a_detailed_error_message = 'A detailed error message'
        error_message: dict = {
          "status": "FAIL",
          "log": {
            "level": "ERROR",
            "message": a_detailed_error_message,
            "subnodes": []
          }
        }
        input_response.json.return_value = error_message
        input_response.text = json.dumps(error_message)

        assert_that(self.response_utils.handle_response) \
            .raises(RestErrorException) \
            .when_called_with(input_response) \
            .starts_with("('A detailed") \
            .is_equal_to("('A detailed error message', <HTTPStatus.BAD_REQUEST: 400>)")

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
