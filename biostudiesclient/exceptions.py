"""
biostudiesclient.exceptions
~~~~~~~~~~~~

This module contains a custom exception definition regarding to BioStudies client library.

:copyright: (c) 2021 by Karoly Erdos.
:license: Apache2, see LICENSE for more details.
"""


class RestErrorException(Exception):
    """ Custom exception dealing with REST error responses. """

    def __init__(self, message, status_code):
        super().__init__(message, status_code)
        self.message = message
        self.status_code = status_code
