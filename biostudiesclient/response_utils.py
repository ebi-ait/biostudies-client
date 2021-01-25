"""
biostudiesclient.response_utils
~~~~~~~~~~~~

This module dealing with HTTP responses.

:copyright: (c) 2021 by Karoly Erdos.
:license: Apache2, see LICENSE for more details.
"""

from dataclasses import dataclass
from http import HTTPStatus
import requests

from biostudiesclient.exceptions import RestErrorException

TRY_IT_AGAIN_LATER_MESSAGE = "The request to the BioStudies service returned a HTTP Server error." \
                             "Please check the health of the BioStudies service, you may need to resubmit your request"


class ResponseUtils:
    """ Utility class for handling API Response from BioStudies REST API """

    @staticmethod
    def handle_response(input_response):
        """
        Handling the response coming from BioStudies REST API.
        The response always contains the status of the original response.
        If the status is 2xx, then it will contain the response in a JSON format,
        otherwise it raises an exception containing original response's status code
        and the error message from the original response, if there was any, if not
        then a custom error message.

        :param input_response: BioStudies REST API's HTTP response
        :return: Response from BioStudies API with the session id or the error message included
        :rtype biostudiesclient.response_utils.ResponseObject
        :raise RestErrorException if the original response was not containig a successful response
        """

        response = ResponseObject()
        response_json = {}
        if input_response.status_code != requests.codes['internal_server_error']:
            response_json = ResponseUtils.__get_response_json(input_response)
        error_message = ''

        if input_response.status_code == requests.codes['not_found']:
            error_message = f'This URL {input_response.url} not exists. Please, try to correct the requested URL.'
        elif input_response.status_code == requests.codes['internal_server_error']:
            error_message = TRY_IT_AGAIN_LATER_MESSAGE
        elif input_response.status_code not in \
                [requests.codes['ok'], requests.codes['created'], requests.codes['accepted'],
                 requests.codes['no_content']]:
            error_message = ResponseUtils.__get_error_message(response_json)
            if not error_message:
                error_message = TRY_IT_AGAIN_LATER_MESSAGE

        if error_message:
            raise RestErrorException(error_message, input_response.status_code)

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
    """
    A data class for wrapping BioStudies response for any requests.
    It always contains the status of the original response.
    If the status is 200 OK, then it will contain the response in a JSON format,
    otherwise it would contain the error message from the response.
    """

    status = HTTPStatus.OK
    json = {}
