import unittest
from http import HTTPStatus

from mock import patch

from biostudiesclient.api import Api
from biostudiesclient.response_utils import TRY_IT_AGAIN_LATER_MESSAGE, WRONG_REQUEST_URL_MESSAGE
from biostudiesclient.rest_error_exception import RestErrorException
from tests.test_utils import TestUtils


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        self.session_id = 'test.session.id'
        self.api = Api(session_id=self.session_id)

    @patch('biostudiesclient.api.requests.post')
    def test_when_request_wrong_url_then_returns_not_found_response(self, mock_post):
        url = 'http://example.com/wrong/path'
        folder_name = "test_folder"
        error_response = {
            "timestamp": "2021-01-18T14:53:09.309+00:00",
            "status": 404,
            "error": "Not Found",
            "message": "",
            "path": "/not/existing/path"
        }

        mock_post.return_value.status_code = HTTPStatus.NOT_FOUND
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.text = error_response
        mock_post.return_value.url = url

        with self.assertRaises(RestErrorException) as context:
            self.api.create_user_sub_folder(folder_name)

        self.assertEqual(HTTPStatus.NOT_FOUND, context.exception.status_code)
        self.assertEqual(WRONG_REQUEST_URL_MESSAGE.format(URL=url), context.exception.message)

    @patch('biostudiesclient.api.requests.post')
    def test_when_passing_folder_name_then_folder_created(self, mock_post):
        folder_name = "test_folder"

        mock_post.return_value.status_code = HTTPStatus.OK
        mock_post.return_value.json.return_value = {}

        response = self.api.create_user_sub_folder(folder_name)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)
        self.assertFalse(response.error_message)

    @patch('biostudiesclient.api.requests.post')
    def test_when_passing_incorrect_session_id_then_response_with_error(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        folder_name = "test_folder"
        self.session_id = 'incorrect.session.id'

        with self.assertRaises(RestErrorException) as context:
            self.api.create_user_sub_folder(folder_name)

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, context.exception.status_code)
        self.assertEqual(TRY_IT_AGAIN_LATER_MESSAGE, context.exception.message)

    @patch('biostudiesclient.api.requests.post')
    def test_when_upload_a_file_then_returns_ok_response(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.OK
        mock_post.return_value.json.return_value = {}

        file_path = "tests/resources/test_file.txt"

        response = self.api.upload_file(file_path)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)
        self.assertFalse(response.error_message)

    @patch('biostudiesclient.api.requests.post')
    def test_when_upload_a_file_with_wrong_header_then_returns_error_response(self, mock_post):
        expected_error_message = "Current request is not a multipart request"
        file_path = "tests/resources/test_file.txt"
        error_response = {"status": "FAIL",
                          "log": {"level": "ERROR",
                                  "message": expected_error_message,
                                  "subnodes": []}}

        mock_post.return_value.status_code = HTTPStatus.BAD_REQUEST
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.text = error_response

        with self.assertRaises(RestErrorException) as context:
            self.api.upload_file(file_path)

        self.assertEqual(HTTPStatus.BAD_REQUEST, context.exception.status_code)
        self.assertEqual(expected_error_message, context.exception.message)

    @patch('biostudiesclient.api.requests.get')
    def test_when_request_user_files_then_returns_correct_response(self, mock_get):
        user_files_response = self.__get_user_files_response()

        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.json.return_value = user_files_response
        mock_get.return_value.text = user_files_response

        response = self.api.get_user_files()

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(len(response.json), 4)
        self.assertEqual(response.json, user_files_response)
        self.assertFalse(response.error_message)

    @patch('biostudiesclient.api.requests.delete')
    def test_when_delete_user_files_then_returns_correct_response(self, mock_delete):
        mock_delete.return_value.status_code = HTTPStatus.OK
        mock_delete.return_value.json.return_value = {}

        file_name = "test_file.txt"

        response = self.api.delete_file(file_name)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertFalse(response.json)
        self.assertFalse(response.error_message)

    # TODO Whenever Biostudies correct their API and returns the correct HTTP Status Code
    # when a file is not available for deletion then write a test against it
    # currently they return 200 OK, even if the file not exists

    @patch('biostudiesclient.api.requests.post')
    def test_when_post_a_submission_then_returns_correct_response(self, mock_post):
        submission_response = self.__get_submission_response_without_file()
        mock_post.return_value.status_code = HTTPStatus.OK
        mock_post.return_value.json.return_value = submission_response
        mock_post.return_value.text = submission_response

        metadata = TestUtils.create_metadata_for_submission_without_file()

        response = self.api.create_submission(metadata)

        self.assertEqual(response.status, HTTPStatus.OK)

        response_json = response.json

        self.assertTrue(response_json)
        self.assertEqual(response_json['accno'], submission_response['accno'])
        self.assertFalse(response.error_message)

    @patch('biostudiesclient.api.requests.post')
    def test_when_post_a_submission_with_not_existing_file_then_returns_error_response(self, mock_post):
        expected_error_message = "Submission validation errors. File not found: raw_reads_1.xlsx."

        submission_response = self.__get_submission_response_for_not_existing_file()
        mock_post.return_value.status_code = HTTPStatus.BAD_REQUEST
        mock_post.return_value.json.return_value = submission_response
        mock_post.return_value.text = submission_response

        metadata = TestUtils.create_metadata_for_submission_with_a_file()

        with self.assertRaises(RestErrorException) as context:
            self.api.create_submission(metadata)

        self.assertEqual(HTTPStatus.BAD_REQUEST, context.exception.status_code)
        self.assertEqual(expected_error_message, context.exception.message)

    @staticmethod
    def __get_user_files_response():
        return [
            {
                "name": "7f03654c-fb19-4a17-b16b-740d5ad78bd0",
                "path": "user",
                "size": 4096,
                "type": "DIR"
            },
            {
                "name": "raw_reads_1.xlsx",
                "path": "user",
                "size": 19110,
                "type": "FILE"
            },
            {
                "name": "fff25c6a-d2d9-496f-aefe-882a2a787ae1",
                "path": "user",
                "size": 4096,
                "type": "DIR"
            },
            {
                "name": "5200400d-9f45-4c79-83b8-537373fa4c5f",
                "path": "user",
                "size": 4096,
                "type": "DIR"
            }
        ]

    # @staticmethod
    # def __create_metadata_for_submission_without_file():
    #     return {
    #         "attachTo": "Phoenix Project",
    #         "attributes": [
    #             {
    #                 "name": "Title",
    #                 "value": "phoenix submission example"
    #             },
    #             {
    #                 "name": "Description",
    #                 "value": "This is the description of a test phoenix submssion."
    #             }
    #         ],
    #         "section": {
    #             "accno": "Project",
    #             "type": "Study",
    #             "attributes": [
    #                 {
    #                     "name": "Title",
    #                     "value": "Cells of the adult human heart"
    #                 },
    #                 {
    #                     "name": "Description",
    #                     "value": "Cardiovascular disease is the leading cause of death worldwide."
    #                 },
    #                 {
    #                     "name": "Organism",
    #                     "value": "Homo sapiens (human)"
    #                 },
    #                 {
    #                     "name": "alias",
    #                     "value": "Phoenix-test-1"
    #                 }
    #             ],
    #             "files": [
    #             ],
    #             "links": [
    #                 {
    #                     "url": "ABC123",
    #                     "attributes": [
    #                         {
    #                             "name": "type",
    #                             "value": "gen"
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "url": "SAMEA7249626",
    #                     "attributes": [
    #                         {
    #                             "name": "Type",
    #                             "value": "BioSample"
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "subsections": [
    #                 {
    #                     "type": "Author",
    #                     "attributes": [
    #                         {
    #                             "name": "Name",
    #                             "value": "John Doe"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     }
    #
    # @staticmethod
    # def __create_metadata_for_submission_with_a_file():
    #     return {
    #         "attachTo": "Phoenix Project",
    #         "attributes": [
    #             {
    #                 "name": "Title",
    #                 "value": "phoenix submission example"
    #             },
    #             {
    #                 "name": "Description",
    #                 "value": "This is the description of a test phoenix submssion."
    #             }
    #         ],
    #         "section": {
    #             "accno": "Project",
    #             "type": "Study",
    #             "attributes": [
    #                 {
    #                     "name": "Title",
    #                     "value": "Cells of the adult human heart"
    #                 },
    #                 {
    #                     "name": "Description",
    #                     "value": "Cardiovascular disease is the leading cause of death worldwide."
    #                 },
    #                 {
    #                     "name": "Organism",
    #                     "value": "Homo sapiens (human)"
    #                 },
    #                 {
    #                     "name": "alias",
    #                     "value": "Phoenix-test-1"
    #                 }
    #             ],
    #             "files": [
    #                 {
    #                     "path": "raw_reads_1.xlsx",
    #                     "attributes": [
    #                         {
    #                             "name": "Description",
    #                             "value": "Raw Data File"
    #                         }
    #                     ],
    #                     "type": "file"
    #                 }
    #             ],
    #             "links": [
    #                 {
    #                     "url": "ABC123",
    #                     "attributes": [
    #                         {
    #                             "name": "type",
    #                             "value": "gen"
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "url": "SAMEA7249626",
    #                     "attributes": [
    #                         {
    #                             "name": "Type",
    #                             "value": "BioSample"
    #                         }
    #                     ]
    #                 }
    #             ],
    #             "subsections": [
    #                 {
    #                     "type": "Author",
    #                     "attributes": [
    #                         {
    #                             "name": "Name",
    #                             "value": "John Doe"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     }

    @staticmethod
    def __get_submission_response_without_file():
        return {
            "accno": "S-BSST683",
            "attributes": [
                {
                    "name": "Description",
                    "value": "This is the description of a test phoenix submssion."
                },
                {
                    "name": "Title",
                    "value": "phoenix submission example"
                }
            ],
            "section": {
                "accno": "Project",
                "type": "Study",
                "attributes": [
                    {
                        "name": "Title",
                        "value": "Cells of the adult human heart"
                    },
                    {
                        "name": "Description",
                        "value": "Cardiovascular disease is the leading cause of death worldwide."
                    },
                    {
                        "name": "Organism",
                        "value": "Homo sapiens (human)"
                    },
                    {
                        "name": "alias",
                        "value": "Phoenix-test-1"
                    }
                ],
                "links": [
                    {
                        "url": "ABC123",
                        "attributes": [
                            {
                                "name": "type",
                                "value": "gen"
                            }
                        ]
                    },
                    {
                        "url": "SAMEA7249626",
                        "attributes": [
                            {
                                "name": "Type",
                                "value": "BioSample"
                            }
                        ]
                    }
                ],
                "subsections": [
                    {
                        "type": "Author",
                        "attributes": [
                            {
                                "name": "Name",
                                "value": "John Doe"
                            }
                        ]
                    }
                ]
            }
        }

    @staticmethod
    def __get_submission_response_for_not_existing_file():
        return {
            "status": "FAIL",
            "log": {
                "level": "ERROR",
                "message": "Submission validation errors.",
                "subnodes": [
                    {
                        "level": "ERROR",
                        "message": "File not found: raw_reads_1.xlsx.",
                        "subnodes": []
                    }
                ]
            }
        }


if __name__ == '__main__':
    unittest.main()
