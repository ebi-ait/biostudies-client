
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
- create folders and folder structures under the user's root folder,  
- upload a file to the user's root folder   
or a specific folder if the folder parameter has been given by the user,  
- get the list of user's files/folders from the given folder,  
- delete a user's file/folder,  
- send a submission to BioStudies archive with or without data files belong to it,  
- query an existing submission in the BioStudies archive,  
- delete an existing submission from the BioStudies archive.  
  
Authentication/login is always a mandatory first step for the user to get the session Id  
for the follow up requests.  
It only need to do once, then the user can reuse that session ID.  
  
If the user would like to upload files that belongs to a submission,  
then the upload should happen first, after that the submission can be submitted.  
The submission would fail if the user do these steps in the opposite order.  
  
## Prerequisites  
  
- [Python3](https://installpython3.com) should be installed in your environment.  
  
## Installation  
  
        pip install biostudies-client  
  
## Configuration  
  
Before using the library some configuration values need to be set.
This library won't work properly without configuring it in one way or another. 

Currently there are 2 ways to configure the library. 
  
#### Configure with parameters  
  
This is the suggested way to configure the library.  
  
1. Instantiate the Auth class with base URL to BioStudies REST API  
  
```  
auth = Auth('http://example.url.to.biostudies/rest/api')  
```  
  
2. Pass the user's credentials to the login method.  
  
```  
auth.login('username', 'password')  
```  
  
#### Configure with environmental parameters  
  
You can also configure the library by using environmental variables.
You need to set the:
| Environmental variable | Code example |
|--|--|
| URL for BioStudies REST API | ```BIOSTUDIES_API_URL=http://biostudies.url``` |
| username for BioStudies REST API | ```BIOSTUDIES_USERNAME=biostudies_username``` |
| username for BioStudies REST API | ```BIOSTUDIES_PASSWORD=biostudies_password``` |

In this case you don't have to pass any parameter to ```Auth``` class and its ```login``` method.
You can login like this:

```
auth = Auth()
auth.login()
```

## Running the integration tests

1. Require user credentials (user name and password) and 
URL for BioStudies REST API from the BioStudies team [biostudies@ebi.ac.uk](mailto:biostudies@ebi.ac.uk).

2. Use environmental variables for the configuration.
You can find how to do it here: [Configure with environmental parameters](#configure-with-environmental-parameters)

3. Login to EBI VPN using your EBI credentials to be able to access BioStudies DEV or TEST REST API.

4. Execute the following statement

```
python3 -m unittest discover -s tests/integration
```

## Example usage  
  
***NOTE***:  
  
1. If you execute the above examples against BioStudies TEST environment, then you need to login into EBI VPN.
2. All the above code examples using environmental variables for authentication to BioStudies REST API. If you would like to pass the credentials for authentication then please check how to do it in this section: [ Configure with parameters](#configure-with-parameters)

### Login into BioStudies REST API and get the session id using in further requests  
  
```python
from biostudiesclient.auth import Auth  
  
auth = Auth()  
response = auth.login()  
  
# Get the session ID from the response object  
session_id = response.session_id  
  
assert session_id  
  
print(session_id)  
```  
  
### Upload a file into user's root folder in BioStudies archive after authentication  
  
```python
from biostudiesclient.api import Api  

auth = Auth()
auth.login()
api = Api(auth)  
  
file_path = "path/to/test_file.txt"  
  
# Upload the given file  
api.upload_file(file_path)  
```  
  
### Create a folder in user's root folder in BioStudies server after authentication  
  
```python
from biostudiesclient.api import Api  
  
auth = Auth()
auth.login()
api = Api(auth)  
  
folder_name = "test_folder"  
  
# Create the given folder for the user  
api.create_user_sub_folder(folder_name)  
```  
  
### Submit a submission with metadata and file into BioStudies archive after authentication  
  
```python
from biostudiesclient.api import Api  
  
auth = Auth()
auth.login()
api = Api(auth)  
  
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
			"value": "This is the description of a test phoenix submission."
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
				"attributes":[
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
  
assert response.json  
assert response.json['accno']  
  
# print the accession ID of the submission  
print(response.json['accno'])  
```

## Developer Notes

### Publish to PyPI

1. Create PyPI Account through the [registration page](https://pypi.org/account/register/).
    
   Take note that PyPI requires email addresses to be verified before publishing.
   
3. Add a `setup.py` configuration file containing the name and version of the project.

3. Package the project for distribution.
 
        python setup.py sdist
        
    Take note that `setup.py` is configured to build a distribution with name `biostudies-client`.
    Currently this PyPI project is owned privately and may require access rights to change. 
    Alternatively, the project name in `setup.py` can be changed so that it can be built and
    uploaded to a different PyPI entry.
    
4. Install [Twine](https://pypi.org/project/twine/)

        pip install twine        
    
5. Upload the distribution package to PyPI. 

        twine upload dist/*
        
    Running `python setup.py sdist` will create a package in the `dist` directory of the project
    base directory. Specific packages can be chosen if preferred instead of the wildcard `*`:
    
        twine upload dist/biostudies-client-0.1.0.tar