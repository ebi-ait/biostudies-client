from http import HTTPStatus


class TestUtils:

    @staticmethod
    def get_session_id(auth):
        auth_response = auth.login()
        auth_status = auth_response.status

        if auth_status == HTTPStatus.OK:
            return auth_response.session_id

        return auth_response.error_message

    @staticmethod
    def create_metadata_for_submission_without_file():
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
    def create_metadata_for_submission_with_a_file():
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
                        "path": "test_file.txt",
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
