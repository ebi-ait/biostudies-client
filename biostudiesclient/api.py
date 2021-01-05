import requests

from biostudiesclient.response_utils import ResponseUtils
from biostudiesclient.url_paths import CREATE_FOLDER, UPLOAD_FILE, GET_USER_FILES


class Api:

    @staticmethod
    def create_user_sub_folder(session_id, folder_name):
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
    def get_basic_headers(session_id):
        return {
            'X-SESSION-TOKEN': session_id
        }
