"""
biostudiesclient.models
~~~~~~~~~~~~

This module contains the data models for BioStudy entities.

:copyright: (c) 2021 by Karoly Erdos.
:license: Apache2, see LICENSE for more details.
"""

import dataclasses
import json
from dataclasses import dataclass, field
from typing import Set


@dataclass
class BioStudiesAttribute:
    """ Data class with name, value pairs; that represent a generic BioStudy attribute. """
    name: str = None
    value: str = None

    def __hash__(self):
        return hash((self.name, self.value))


@dataclass
class BioStudyFile:
    """ Data class that represent a file for BioStudies archive. """
    path: str = None
    file_type: str = None
    attributes: Set[BioStudiesAttribute] = field(default_factory=set)

    def __hash__(self):
        return hash((self.path, self.file_type))


@dataclass
class BioStudyLink:
    """ Data class that represent a link for BioStudies archive to another entity that might be in another archive. """
    url: str = None
    attributes: Set[BioStudiesAttribute] = field(default_factory=set)

    def __hash__(self):
        return hash(self.url)


@dataclass
class BioStudySubsection:
    """ Data class that represent a sub section inside a submission to BioStudies archive. """
    sub_section_type: str = None
    attributes: Set[BioStudiesAttribute] = field(default_factory=set)

    def __hash__(self):
        return hash(self.sub_section_type)


@dataclass
class BioStudySection:
    """ Data class that represent a section inside a submission to BioStudies archive. """
    section_type: str = None
    accno: str = None
    attributes: Set[BioStudiesAttribute] = field(default_factory=set)
    files: Set[BioStudyFile] = field(default_factory=set)
    links: Set[BioStudyLink] = field(default_factory=set)
    subsections: Set[BioStudySubsection] = field(default_factory=set)


@dataclass
class BioStudy:
    """ Data class that represent the highest level of a BioStudies submission. """
    accno: str = None
    attach_to: str = None
    attributes: Set[BioStudiesAttribute] = field(default_factory=set)
    section: BioStudySection = None


class EnhancedJSONEncoder(json.JSONEncoder):
    """ JSON encoder for the BioStudy data class. """
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if isinstance(o, set):
            return list(o)

        return super().default(o)
