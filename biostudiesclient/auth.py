"""This module dealing with authentication"""

from dataclasses import dataclass
from http import HTTPStatus
import requests

from biostudiesclient.config import BIOSTUDIES_USERNAME, BIOSTUDIES_PASSWORD, BIOSTUDIES_API_URL


# This class dealing with authentication.
# It is using the provided credentials to login to BioStudies.
class Auth:
    def __init__(self):
        self.username = BIOSTUDIES_USERNAME
        self.password = BIOSTUDIES_PASSWORD
        self.login_url = f'{BIOSTUDIES_API_URL}/auth/login'

    def login(self):
        response = requests.post(self.login_url, json=self.login_payload())
        response_json = response.json()
        response_status = response.status

        auth_response = AuthResponse(status=HTTPStatus(response_status))
        if response_status == HTTPStatus.OK:
            auth_response.session_id = response_json["sessid"]
        else:
            auth_response.error_message = response_json["log"]["message"]

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
