import requests

from biostudiesclient.response_utils import ResponseUtils
from biostudiesclient.url_paths import CREATE_FOLDER, UPLOAD_FILE


class Api:

    @staticmethod
    def create_user_sub_folder(session_id, folder_name):
        url = CREATE_FOLDER.format(folder_name=folder_name)

        headers = {
            'X-SESSION-TOKEN': session_id
        }
        response = ResponseUtils.handle_response(requests.post(url, headers=headers))

        return response

    @staticmethod
    def upload_file(session_id, file_path):
        url = UPLOAD_FILE

        headers = {
            'X-SESSION-TOKEN': session_id
        }

        file_to_upload = {'file': open(file_path, 'rb')}

        response = ResponseUtils.handle_response(
            requests.post(url, headers=headers, files=file_to_upload))

        return response
