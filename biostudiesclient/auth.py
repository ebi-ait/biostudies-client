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

from biostudiesclient.config import get_username_from_env, get_password_from_env, get_biostudies_base_url_from_env
from biostudiesclient.response_utils import ResponseUtils


class Auth:
    """
    This class dealing with authentication to BioStudies REST API.
    It is using the provided credentials to login to BioStudies API
    and gets the session id from its response.
    """

    def __init__(self, base_url=None):
        self.username = None
        self.password = None
        self.session_id = None
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = get_biostudies_base_url_from_env()

        self.login_url = f'{self.base_url}/auth/login'

    def login(self, username=None, password=None):
        """
        This method tries to send a login request with the configured credentials
        to the BioStudies REST API.
        The URL to send the login request is defined during initialisation.
        The method checks the returned status code from BioStudies REST API.
        In case it is 200 OK, then parse the response and gets the session id from it.
        Otherwise it gets the error message from the response.
        :return: Response from BioStudies API with the session id or the error message included
        :rtype biostudiesclient.auth.AuthResponse
        """

        self.__set_credentials(username, password)

        response = ResponseUtils.handle_response(requests.post(self.login_url, json=self.__login_payload()))

        auth_response = AuthResponse(status=HTTPStatus(response.status))

        self.session_id = response.json["sessid"]
        auth_response.session_id = self.session_id

        return auth_response

    def __set_credentials(self, username, password):
        self.__initialise_credentials_from_env()

        if username:
            self.username = username
        if password:
            self.password = password

    def __initialise_credentials_from_env(self):
        self.username = get_username_from_env()
        self.password = get_password_from_env()

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
