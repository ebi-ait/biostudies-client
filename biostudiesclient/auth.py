"""
biostudiesclient.auth
~~~~~~~~~~~~

This module dealing with authentication

:copyright: (c) 2021 by Karoly Erdos.
:license: Apache2, see LICENSE for more details.
"""

from dataclasses import dataclass
from http import HTTPStatus
import requests

from biostudiesclient.config import BIOSTUDIES_USERNAME, BIOSTUDIES_PASSWORD, BIOSTUDIES_API_URL
from biostudiesclient.response_utils import ResponseUtils, STATUS_CODE_OK


class Auth:
    """
    This class dealing with authentication to BioStudies REST API.
    It is using the provided credentials to login to BioStudies API
    and gets the session id from its response.
    """

    def __init__(self, login_url=None):
        if login_url:
            self.login_url = login_url
        else:
            self.login_url = f'{BIOSTUDIES_API_URL}/auth/login'

        self.username = BIOSTUDIES_USERNAME
        self.password = BIOSTUDIES_PASSWORD

    def login(self, username=None, password=None):
        """
        This method tries to send a login request with the configured credentials
        to the BioStudies REST API.
        Checks the returned status code. In case it is 200 OK, then parse the response and gets the session id from it.
        Otherwise it gets the error message from the response.
        :return: Response from BioStudies API with the session id or the error message included
        :rtype biostudiesclient.auth.AuthResponse
        """

        self.__set_credentials(username, password)

        response = ResponseUtils.handle_response(requests.post(self.login_url, json=self.__login_payload()))

        auth_response = AuthResponse(status=HTTPStatus(response.status))
        if response.status == STATUS_CODE_OK:
            auth_response.session_id = response.json["sessid"]
        else:
            auth_response.error_message = response.error_message

        return auth_response

    def __set_credentials(self, username, password):
        if username:
            self.username = username
        if password:
            self.password = password

    def __login_payload(self):
        """
        Creates and returns a dictionary with credential information related to login to BioStudies REST API.
        :return a dictionary with the credentials data
        :rtype dict
        """

        return {
            "login": self.username,
            "password": self.password
        }


@dataclass
class AuthResponse:
    """
    A data class for wrapping BioStudies response for an authentication request.
    It always contains the status of the response.
    If the status is 200 OK, then it will contain the session id,
    otherwise it would contain the error message from the response.
    """

    status: HTTPStatus
    session_id: str = ""
    error_message: str = ""
