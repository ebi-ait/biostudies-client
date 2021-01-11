import requests

from biostudiesclient.config import BIOSTUDIES_API_URL
from biostudiesclient.response_utils import ResponseUtils
from biostudiesclient.url_paths import CREATE_FOLDER, UPLOAD_FILE, GET_USER_FILES, DELETE_FILE,\
    CREATE_SUBMISSION


class Api:
    """
    PI client to interact with the BioStudies API.

    You can use this API client class to
    - create a user folder
    - upload a file
    - get the list of user's files
    - delete a user's file
    - send a submission to BioStudies archive
    """

    def __init__(self, session_id):
        self.base_url = BIOSTUDIES_API_URL
        self.session_id = session_id

    def create_user_sub_folder(self, folder_name):
        """
        Create a folder in the user's directory
        :param session_id: required for sending a request to BioStudies' API
        :param folder_name: the name of the folder to be create for the user
        :return: Response from BioStudies API
        """
        url = self.base_url + CREATE_FOLDER.format(folder_name=folder_name)

        headers = Api.get_basic_headers(self.session_id)
        response = ResponseUtils.handle_response(requests.post(url, headers=headers))

        return response

    def upload_file(self, file_path):
        url = self.base_url + UPLOAD_FILE

        headers = Api.get_basic_headers(self.session_id)

        with open(file_path, "rb") as a_file:
            file_dict = {file_path: a_file}
        # file_to_upload = {'upload_file.txt': open(file_path, 'rb')}

            response = ResponseUtils.handle_response(
                requests.post(url, headers=headers, files=file_dict))

        return response

    def get_user_files(self):
        url = GET_USER_FILES
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.get(url, headers=headers))

        return response

    def delete_file(self, file_name):
        url = self.base_url + DELETE_FILE.format(file_name=file_name)
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.delete(url, headers=headers))

        return response

    def create_submission(self, metadata):
        url = CREATE_SUBMISSION
        headers = Api.get_basic_headers(self.session_id)

        response = ResponseUtils.handle_response(
            requests.post(url, headers=headers, json=metadata))

        return response

    @staticmethod
    def get_basic_headers(session_id):
        return {
            'X-SESSION-TOKEN': session_id
        }
