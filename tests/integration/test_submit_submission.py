import os
import unittest
from http import HTTPStatus

from biostudiesclient.api import Api
from biostudiesclient.auth import Auth
from biostudiesclient.exceptions import RestErrorException
from tests.test_utils import TestUtils


class TestSubmitSubmission(unittest.TestCase):

    def setUp(self) -> None:
        self.auth = Auth()
        self.auth.login()
        self.api = Api(self.auth)

    def test_when_post_a_submission_without_a_file_then_returns_correct_response(self):
        metadata = TestUtils.create_metadata_for_submission_without_file()

        response = self.api.create_submission(metadata)

        self.assertEqual(response.status, HTTPStatus.OK)

        response_json = response.json

        self.assertTrue(response_json)
        accession_id = response_json['accno']
        self.assertTrue(accession_id)

        self.__clean_up(accession_id)

    def test_when_query_an_existing_submission_then_returns_correct_response(self):
        metadata = TestUtils.create_metadata_for_submission_without_file()

        create_response = self.api.create_submission(metadata)

        self.assertEqual(create_response.status, HTTPStatus.OK)

        response_json = create_response.json
        accession_id = response_json['accno']

        get_response = self.api.get_submission(accession_id)

        self.assertEqual(get_response.status, HTTPStatus.OK)

        get_response_json = get_response.json

        self.assertTrue(get_response_json)
        self.assertEqual(accession_id, get_response_json['accno'])

        self.__clean_up(accession_id)

    def test_post_a_submission_with_a_file_in_metadata_but_without_uploading_the_file_then_returns_error_response(self):
        expected_error_message_for_missing_file = 'Submission validation errors File not found: test_file.txt'

        metadata_with_file = TestUtils.create_metadata_for_submission_with_a_file()

        with self.assertRaises(RestErrorException) as context:
            self.api.create_submission(metadata_with_file)

        self.assertEqual(expected_error_message_for_missing_file, context.exception.message)
        self.assertEqual(HTTPStatus.BAD_REQUEST, context.exception.status_code)

    def test_when_post_a_submission_with_a_file_then_returns_correct_response(self):
        folder1 = 'sub1'
        txt_folder_name = '{}/txt_files'.format(folder1)

        self.api.create_user_sub_folder(txt_folder_name)

        file_path = "tests/resources/test_file.txt"

        self.api.upload_file(file_path, txt_folder_name)

        metadata_with_file = TestUtils.create_metadata_for_submission_with_a_file()
        metadata_with_file['section']['files'][0]['path'] = txt_folder_name + '/test_file.txt'

        response = self.api.create_submission(metadata_with_file)

        self.assertEqual(response.status, HTTPStatus.OK)
        response_json = response.json
        self.assertTrue(response_json)
        accession_id = response_json['accno']
        self.assertTrue(accession_id)

        # clean up the submission and the file
        self.__clean_up(accession_id)
        self.api.delete_file(os.path.basename(folder1))

    def __clean_up(self, accession_id):
        self.api.delete_submission(accession_id)


if __name__ == '__main__':
    unittest.main()
