import unittest
from http import HTTPStatus

from mock import patch

from biostudiesclient.api import Api
from biostudiesclient.response_utils import TRY_IT_AGAIN_LATER_MESSAGE, WRONG_REQUEST_URL_MESSAGE


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        self.api = Api()

    @patch('biostudiesclient.api.requests.post')
    def test_when_request_wrong_url_then_returns_not_found_response(self, mock_post):
        url = 'http://example.com/wrong/path'
        folder_name = "test_folder"
        session_id = 'test.session.id'

        mock_post.return_value.status_code = HTTPStatus.NOT_FOUND
        mock_post.return_value.url = url

        response = self.api.create_user_sub_folder(session_id, folder_name)

        self.assertEqual(response.status, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.error_message, WRONG_REQUEST_URL_MESSAGE.format(URL=url))

    @patch('biostudiesclient.api.requests.post')
    def test_when_passing_folder_name_then_folder_created(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.OK

        folder_name = "test_folder"
        session_id = 'test.session.id'

        response = self.api.create_user_sub_folder(session_id, folder_name)

        self.assertEqual(response.status, HTTPStatus.OK)

    @patch('biostudiesclient.api.requests.post')
    def test_when_passing_incorrect_session_id_then_response_with_error(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        folder_name = "test_folder"
        session_id = 'incorrect.session.id'

        response = self.api.create_user_sub_folder(session_id, folder_name)

        self.assertEqual(response.status, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.error_message, TRY_IT_AGAIN_LATER_MESSAGE)

    @patch('biostudiesclient.api.requests.post')
    def test_when_upload_a_file_then_returns_ok_response(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.OK

        file_path = "resources/test_file.txt"
        session_id = 'test.session.id'

        response = self.api.upload_file(session_id, file_path)

        self.assertEqual(response.status, HTTPStatus.OK)

    @patch('biostudiesclient.api.requests.post')
    def test_when_upload_a_file_with_wrong_header_then_returns_error_response(self, mock_post):
        mock_post.return_value.status_code = HTTPStatus.BAD_REQUEST

        file_path = "resources/test_file.txt"
        session_id = 'test.session.id'

        response = self.api.upload_file(session_id, file_path)

        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)

    @patch('biostudiesclient.api.requests.get')
    def test_when_request_user_files_then_returns_correct_response(self, mock_get):
        user_files_response = [
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

        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.json.return_value = user_files_response

        session_id = 'test.session.id'

        response = self.api.get_user_files(session_id)

        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(len(response.json), 4)
        self.assertEqual(response.json, user_files_response)

    @patch('biostudiesclient.api.requests.delete')
    def test_when_delete_user_files_then_returns_correct_response(self, mock_delete):
        mock_delete.return_value.status_code = HTTPStatus.OK

        file_name = "test_file.txt"
        session_id = 'test.session.id'

        response = self.api.delete_file(session_id, file_name)

        self.assertEqual(response.status, HTTPStatus.OK)

    # TODO Whenever Biostudies correct their API and returns the correct HTTP Status Code
    # when a file is not available for deletion then write a test against it
    # currently they return 200 OK, even if the file not exists

    @patch('biostudiesclient.api.requests.post')
    def test_when_post_a_submission_then_returns_correct_response(self, mock_post):
        submission_response = self.__get_submission_response_without_file()
        mock_post.return_value.status_code = HTTPStatus.OK
        mock_post.return_value.json.return_value = submission_response

        session_id = 'test.session.id'
        metadata = self.__create_metadata_for_submission_without_file()

        response = self.api.create_submission(session_id, metadata)

        self.assertEqual(response.status, HTTPStatus.OK)

        response_json = response.json

        self.assertEqual(response_json['accno'], submission_response['accno'])

    @patch('biostudiesclient.api.requests.post')
    def test_when_post_a_submission_with_not_existing_file_then_returns_error_response(self, mock_post):
        submission_response = self.__get_submission_response_for_not_existing_file()
        mock_post.return_value.status_code = HTTPStatus.BAD_REQUEST
        mock_post.return_value.json.return_value = submission_response

        session_id = 'test.session.id'
        metadata = self.__create_metadata_for_submission_with_a_file()

        response = self.api.create_submission(session_id, metadata)

        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)
        self.assertFalse(response.json)
        self.assertEqual(
            "Submission validation errors. File not found: raw_reads_1.xlsx.",
            response.error_message)

    @staticmethod
    def __create_metadata_for_submission_without_file():
        return {
            "attachTo": "Phoenix Project",
            "attributes": [
                {
                    "name": "Title",
                    "value": "phoenix submission example"
                },
                {
                    "name": "Description",
                    "value": "This is the description of a test phoenix submssion."
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
                "files": [
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
    def __create_metadata_for_submission_with_a_file():
        return {
            "attachTo": "Phoenix Project",
            "attributes": [
                {
                    "name": "Title",
                    "value": "phoenix submission example"
                },
                {
                    "name": "Description",
                    "value": "This is the description of a test phoenix submssion."
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
                "files": [
                    {
                        "path": "raw_reads_1.xlsx",
                        "attributes": [
                            {
                                "name": "Description",
                                "value": "Raw Data File"
                            }
                        ],
                        "type": "file"
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
