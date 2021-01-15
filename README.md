[![Build Status](https://travis-ci.org/ebi-ait/biostudies-client.svg?branch=main)](https://travis-ci.org/ebi-ait/biostudies-client.svg?branch=main)

# BioStudies-client - Python library

This library aims to provide a Python client to access/wrap BioStudies REST API.

The client is under development, so any contribution encouraged and welcome.
Please, create a branch from the latest main branch,
do your modification(s) and create a Pull Request against the latest main branch.
We are going to review it and after careful consideration
we might merge it into the main branch.  

## Overview 

This API client can be used to do the followings:

- authenticate to BioStudies REST API with the provided credentials,
- create folders under the user's root folder,
- upload a file to the user's folder,
- get the list of user's files/folders,
- delete a user's file/folder,
- send a submission to BioStudies archive with or without data files belong to it,
- query an existing submission in the BioStudies archive,
- delete an existing submission from the BioStudies archive.

Authentication/login is always a mandatory first step for the user to get the session Id
for the follow up requests.
It only need to do once, then the user can reuse that session ID.

If the user would like to upload files that belongs to a submission,
then the upload should happen first then the submission can be submitted.
The submission would fail if the user do these steps in the opposite way. 

## Prerequisites

- [Python3](https://installpython3.com)

## Installation

TODO: Add installation method here

## Required setup

Before using the library some environmental variables like the URL for BioStudies REST API,
and the credentials (username, password) for it need to be configured.

```
BIOSTUDIES_API_URL=http://biostudies.url
BIOSTUDIES_USERNAME=biostudies_username
BIOSTUDIES_PASSWORD=biostudies_password
```

This library won't work properly without configuring this variables.

## Example usage

***NOTE***:

    If you execute the above examples against BioStudies TEST environment,
    then you need to login into EBI VPN. 

### Login into BioStudies REST API and get the session id using in further requests

```
from biostudiesclient.auth import Auth

auth = Auth()
response = auth.login()

# Get the session ID from the response object
session_id = response.session_id

assert session_id

print(session_id)
```

### Upload a file into user's root folder in BioStudies archive after authentication

```
from biostudiesclient.api import Api

api = Api(session_id=<users_session_id>)

file_path = "path/to/test_file.txt"

# Upload the given file
response = api.upload_file(file_path)

assert response.status == HTTPStatus.OK
assert len(response.error_message) == 0
```

### Create a folder in user's root folder in BioStudies server after authentication

```
from biostudiesclient.api import Api

api = Api(session_id=<users_session_id>)

folder_name = "test_folder"

# Create the given folder for the user
response = api.create_user_sub_folder(folder_name)

assert response.status == HTTPStatus.OK
assert len(response.error_message) == 0
```

### Submit a submission with metadata and file into BioStudies archive after authentication

```
from biostudiesclient.api import Api

api = Api(session_id=<users_session_id>)

# Upload the given file
file_path = "path/to/test_file.txt"
api.upload_file(file_path)

metadata = {
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

# submit the submission
response = api.create_submission(metadata)

assert response.status == HTTPStatus.OK
assert response.json
assert response.json['accno']

# print the accession ID of the submission
print(response.json['accno'])
```
