"""
biostudiesclient.api
~~~~~~~~~~~~

This module implements an API that interact with the BioStudies REST API.

:copyright: (c) 2021 by Karoly Erdos.
:license: Apache2, see LICENSE for more details.
"""


import os
import requests

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
    - create a user folder or folder structure
    - upload a file to the user's root folder
    or a specific folder if the folder parameter has been given by the user
    - get the list of user's files from the given folder
    - delete a user's file
    - send a submission to BioStudies archive
    - query an existing submission in the BioStudies archive
    - delete an existing submission from the BioStudies archive
    """

    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.base_url

    def create_user_sub_folder(self, folder_name):
        """
        Create a folder in the user's directory.
        The name of the folder could be a single folder
        or a deeper folder structure like: 'folder1/folder2/folder3'.
        :param folder_name: the name of the folder or folder structure to be create for the user
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + CREATE_FOLDER.format(folder_name=folder_name)

        headers = self.get_basic_headers()
        response = ResponseUtils.handle_response(requests.post(url, headers=headers))

        return response

    def upload_file(self, file_path, folder_path=None):
        """
        Upload a file from the given file path into the user's folder or sub-folder
        :param file_path: the path of the file locally where it can be accessed for upload
        :param folder_path: the path of the sub folders in the user's folder on the server
                            where the file will be uploaded.
                            It should be in the format of 'folder1/folder2/folder3'.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + UPLOAD_FILE

        if folder_path:
            url = '/'.join([url, folder_path])

        headers = self.get_basic_headers()

        with open(file_path, "rb") as a_file:
            file_dict = [(
                'files',
                (os.path.basename(file_path), a_file)
            )]

            response = ResponseUtils.handle_response(
                requests.post(url, headers=headers, files=file_dict))

        return response

    def get_user_files(self, folder_path=None):
        """
        Get the list of files and folders from the user's root directory
        if the folder_path parameter is empty,
        otherwise return the contents of the user's sub folder structure defined by
        the value of the given parameter.

        :param folder_path: the path of the sub folders in the user's folder on the server.
                            It should be in the format of 'folder1/folder2/folder3'.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + GET_USER_FILES

        if folder_path:
            url = '/'.join([url, folder_path])

        headers = self.get_basic_headers()

        response = ResponseUtils.handle_response(
            requests.get(url, headers=headers))

        return response

    def delete_file(self, file_name):
        """
        Delete a file/folder with the given file/folder name from the user's root folder or sub-folder path.
        :param file_name:   the name of the file or folder to be deleted.
                            If it is a folder that needs to be deleted,
                            then the parameter's value should be in the format of 'folder1/folder2/folder3'.
        :return: Response from BioStudies API
        :rtype biostudiesclient.response_utils.ResponseObject
        """

        url = self.base_url + DELETE_FILE.format(file_name=file_name)
        headers = self.get_basic_headers()

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
        headers = self.get_basic_headers()
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
        headers = self.get_basic_headers()

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
        headers = self.get_basic_headers()

        response = ResponseUtils.handle_response(
            requests.delete(url, headers=headers))

        return response

    def session_id(self):
        """
        Gets session id from Auth object.
        :return: Session id from Auth object.
        """
        return self.auth.session_id

    def get_basic_headers(self):
        """
        Creates and returns a dictionary with the session id parameter
        for the HTTP header request.
        :param session_id: session id for the HTTP request to be created
        :return a dictionary with a session id
        :rtype dict
        """

        return {
            'X-SESSION-TOKEN': self.session_id()
        }
