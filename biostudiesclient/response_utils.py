from dataclasses import dataclass
from http import HTTPStatus

STATUS_CODE_OK = 200
STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_NOT_FOUND = 404
STATUS_CODE_UNAUTHORIZED = 401
STATUS_CODE_INTERNAL_SERVER_ERROR = 500

TRY_IT_AGAIN_LATER_MESSAGE = "Unknown error happened. Please, try it again later."
WRONG_REQUEST_URL_MESSAGE = "This URL {URL} not exists. Please, try to correct the requested URL."


class ResponseUtils:

    @staticmethod
    def handle_response(input_response):
        response = ResponseObject()
        response_json = ResponseUtils.__get_response_json(input_response)
        if input_response.status_code == STATUS_CODE_INTERNAL_SERVER_ERROR:
            response.error_message = TRY_IT_AGAIN_LATER_MESSAGE
        elif input_response.status_code == STATUS_CODE_NOT_FOUND:
            response.error_message = WRONG_REQUEST_URL_MESSAGE.format(URL=input_response.url)
        elif input_response.status_code == STATUS_CODE_UNAUTHORIZED:
            error_message = ResponseUtils.__get_error_message(response_json)
            response.error_message = error_message if error_message else TRY_IT_AGAIN_LATER_MESSAGE
        elif input_response.status_code == STATUS_CODE_BAD_REQUEST:
            response.error_message = ResponseUtils.__get_error_message(response_json)
        elif input_response.status_code == STATUS_CODE_OK:
            response.json = response_json

        response.status = input_response.status_code

        return response

    @staticmethod
    def __get_response_json(input_response):
        if len(input_response.text) == 0:
            return ''

        return input_response.json()

    @staticmethod
    def __get_error_message(response_json):
        message = response_json["log"]["message"]
        detailed_messages = response_json["log"]["subnodes"]
        if detailed_messages:
            for additional_message in detailed_messages:
                message += " " + additional_message['message']
        if not message:
            message = response_json["message"]

        return message


@dataclass
class ResponseObject:
    status = HTTPStatus.OK
    error_message = ""
    json = {}
