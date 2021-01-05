from dataclasses import dataclass
from http import HTTPStatus

TRY_IT_AGAIN_LATER_MESSAGE = "Unknown error happened. Please, try it again later."
WRONG_REQUEST_URL_MESSAGE = "This URL {URL} not exists. Please, try to correct the requested URL."


class ResponseUtils:

    @staticmethod
    def handle_response(input_response):
        response = ResponseObject
        if input_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            response.error_message = TRY_IT_AGAIN_LATER_MESSAGE
        elif input_response.status_code == HTTPStatus.NOT_FOUND:
            response.error_message = WRONG_REQUEST_URL_MESSAGE.format(URL=input_response.url)
        elif input_response.status_code == HTTPStatus.UNAUTHORIZED:
            message = input_response["log"]["message"]
            if message:
                response.error_message = message
            else:
                message = input_response["message"]
                response.error_message = message if message else TRY_IT_AGAIN_LATER_MESSAGE
        elif input_response.status_code == HTTPStatus.BAD_REQUEST:
            response.error_message = input_response["log"]["message"]
        elif input_response.status_code == HTTPStatus.OK:
            response.json = input_response.text

        response.status = input_response.status_code

        return response


@dataclass
class ResponseObject:
    status: HTTPStatus
    error_message: str
    json: dict
