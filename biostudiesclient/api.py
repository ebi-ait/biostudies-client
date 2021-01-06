import requests

from biostudiesclient.response_utils import ResponseUtils
from biostudiesclient.url_paths import CREATE_FOLDER, UPLOAD_FILE, GET_USER_FILES, DELETE_FILE


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

    @staticmethod
    def create_user_sub_folder(session_id, folder_name):
        """
        Create a folder in the user's directory
        :param session_id: required for sending a request to BioStudies' API
        :param folder_name: the name of the folder to be create for the user
        :return: Response from BioStudies API
        """
        url = CREATE_FOLDER.format(folder_name=folder_name)

        headers = Api.get_basic_headers(session_id)
        response = ResponseUtils.handle_response(requests.post(url, headers=headers))

        return response

    @staticmethod
    def upload_file(session_id, file_path):
        url = UPLOAD_FILE

        headers = Api.get_basic_headers(session_id)

        file_to_upload = {'file': open(file_path, 'rb')}

        response = ResponseUtils.handle_response(
            requests.post(url, headers=headers, files=file_to_upload))

        return response

    @staticmethod
    def get_user_files(session_id):
        url = GET_USER_FILES
        headers = Api.get_basic_headers(session_id)

        response = ResponseUtils.handle_response(
            requests.get(url, headers=headers))

        return response

    @staticmethod
    def delete_file(session_id, file_name):
        url = DELETE_FILE.format(file_name=file_name)
        headers = Api.get_basic_headers(session_id)

        response = ResponseUtils.handle_response(
            requests.delete(url, headers=headers))

        return response

    @staticmethod
    def get_basic_headers(session_id):
        return {
            'X-SESSION-TOKEN': session_id
        }
