"""
biostudiesclient.api
~~~~~~~~~~~~

This module implements an API that interact with the BioStudies REST API.

:copyright: (c) 2021 by Karoly Erdos.
:license: Apache2, see LICENSE for more details.
"""


import os
import requests

from biostudiesclient.config import BIOSTUDIES_API_URL
from biostudiesclient.response_utils import ResponseUtils

LOGIN_TO_BST = '/auth/login'
CREATE_FOLDER = '/folder/user?folder={folder_name}'
UPLOAD_FILE = '/files/user'
GET_USER_FILES = '/files/user'
DELETE_FILE = '/files/user?fileName={file_name}'
CREATE_SUBMISSION = '/submissions'
GET_SUBMISSION_BY_ACCESSION_ID = '/submissions/{accession_id}.json'
DELETE_SUBMISSION = '/submissions/{accession_id}'


class Api:
    """
    This class responsibility to interact with the BioStudies API.

    You can use this API client class to
    - create a user folder
    - upload a file
    - get the list of user's files
    - delete a user's file
    - send a submission to BioStudies archive
    - query an existing submission in the BioStudies archive
    - delete an existing submission from the BioStudies archive
    """

    def __init__(self, session_id):
        self.base_url = BIOSTUDIES_API_URL
        self.session_id = session_id

    def create_user_sub_folder(self, folder_name):
        """
        Create a folder in the user's directory
        :param folder_name: the name of the folder to be create for the user
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + CREATE_FOLDER.format(folder_name=folder_name)

        headers = Api.get_basic_headers(self.session_id)
        response = ResponseUtils.handle_response(requests.post(url, headers=headers))

        return response

    def upload_file(self, file_path):
        """
        Upload a file from the given file path into the user's directory
        :param file_path: the path of the file where it can be accessed for upload
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + UPLOAD_FILE

        headers = Api.get_basic_headers(self.session_id)

        with open(file_path, "rb") as a_file:
            file_dict = [(
                'files',
                (os.path.basename(file_path), a_file)
            )]

            response = ResponseUtils.handle_response(
                requests.post(url, headers=headers, files=file_dict))

        return response

    def get_user_files(self):
        """
        Get the list of files and folders from the user's root directory.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = GET_USER_FILES
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.get(url, headers=headers))

        return response

    def delete_file(self, file_name):
        """
        Delete a file with the given file name from the user's directory
        :param file_name: the name of the file to be delete
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + DELETE_FILE.format(file_name=file_name)
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.delete(url, headers=headers))

        return response

    def create_submission(self, metadata):
        """
        Create and submit a submission with the given metadata.
        In the metadata the user can include a list of files, too.
        :param metadata: Contains all the metadata belongs to a submission.
        The metadata optionally can contain information of files that belongs to this submission.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + CREATE_SUBMISSION
        headers = Api.get_basic_headers(self.session_id)
        headers.update({'Submission_Type': 'application/json'})

        response = ResponseUtils.handle_response(
            requests.post(url, headers=headers, json=metadata))

        return response

    def get_submission(self, accession_id):
        """
        Get all the metadata information of a specific submission given by the accession id parameter.
        :param accession_id: accession id of the queried submission.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + GET_SUBMISSION_BY_ACCESSION_ID.format(accession_id=accession_id)
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.get(url, headers=headers))

        return response

    def delete_submission(self, accession_id):
        """
        Delete a specific submission from the BioStudies archive given by the accession id parameter.
        :param accession_id: accession id of the queried submission.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + DELETE_SUBMISSION.format(accession_id=accession_id)
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.delete(url, headers=headers))

        return response

    @staticmethod
    def get_basic_headers(session_id):
        """
        Creates and returns a dictionary with the session id parameter
        for the HTTP header request.
        :param session_id: session id for the HTTP request to be created
        :return a dictionary with a session id
        :rtype dict
        """

        return {
            'X-SESSION-TOKEN': session_id
        }
