"""This module dealing with authentication"""

from dataclasses import dataclass
from http import HTTPStatus
import requests

from biostudiesclient.config import BIOSTUDIES_USERNAME, BIOSTUDIES_PASSWORD, BIOSTUDIES_API_URL
from biostudiesclient.response_utils import STATUS_CODE_OK


# This class dealing with authentication.
# It is using the provided credentials to login to BioStudies.
from biostudiesclient.response_utils import ResponseUtils


class Auth:
    def __init__(self):
        self.username = BIOSTUDIES_USERNAME
        self.password = BIOSTUDIES_PASSWORD
        self.login_url = f'{BIOSTUDIES_API_URL}/auth/login'

    def login(self):
        response = ResponseUtils.handle_response(requests.post(self.login_url, json=self.login_payload()))

        auth_response = AuthResponse(status=HTTPStatus(response.status))
        if response.status == STATUS_CODE_OK:
            auth_response.session_id = response.json["sessid"]
        else:
            auth_response.error_message = response.error_message

        return auth_response

    def login_payload(self):
        return {
            "login": self.username,
            "password": self.password
        }


@dataclass
class AuthResponse:
    status: HTTPStatus
    session_id: str = ""
    error_message: str = ""
