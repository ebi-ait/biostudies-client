""" Contains configuration entries for biostudies client. """

import os


def get_biostudies_base_url_from_env():
    biostudies_api_url_dev = 'http://biostudy-dev:8788'
    return os.environ.get('BIOSTUDIES_API_URL', biostudies_api_url_dev)


def get_username_from_env():
    biostudies_username_dev = 'CHANGE_ME'
    return os.environ.get('BIOSTUDIES_USERNAME', biostudies_username_dev)


def get_password_from_env():
    biostudies_password_dev = 'CHANGE_ME'
    return os.environ.get('BIOSTUDIES_PASSWORD', biostudies_password_dev)
