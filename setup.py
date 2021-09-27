""" Configuration file for deployment """

import os

from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)
install_requires = [line.rstrip() for line in open(os.path.join(base_dir, 'requirements.txt'))]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='biostudies-client',
    version='0.1.4',
    description="Python client library for wrapping and handling BioStudies REST API calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebi-ait/biostudies-client",
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
