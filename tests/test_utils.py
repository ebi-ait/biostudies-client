import json

from biostudiesclient.models import BioStudy, BioStudySection, BioStudiesAttribute, BioStudyLink, BioStudySubsection, \
    EnhancedJSONEncoder, BioStudyFile


class TestUtils:

    @staticmethod
    def create_metadata_for_submission_without_file():
        bio_study = TestUtils.create_bio_study_without_file()

        json_payload = TestUtils.create_json_payload_from_bio_study(bio_study)

        return json_payload

    @staticmethod
    def create_metadata_for_submission_with_a_file():
        bio_study = TestUtils.create_bio_study_without_file()

        bio_study.section.files.add(
            TestUtils.create_bio_study_file("test_file.txt", "BAM",
                                            {TestUtils.create_attribute("Description", "Raw Data File")})
        )

        json_payload = TestUtils.create_json_payload_from_bio_study(bio_study)

        return json_payload

    @staticmethod
    def create_json_payload_from_bio_study(bio_study):
        return json.loads(json.dumps(bio_study, cls=EnhancedJSONEncoder))

    @staticmethod
    def create_bio_study_without_file():
        bio_study = BioStudy()
        bio_study.attach_to = "Phoenix Project"

        bio_study.attributes.add(
            TestUtils.create_attribute("Title", "phoenix submission example"))
        bio_study.attributes.add(
            TestUtils.create_attribute("Description", "This is the description of a test phoenix submission"))

        bio_study_section = BioStudySection()
        bio_study_section.accno = "Project"
        bio_study_section.section_type = "Study"

        bio_study_section.attributes.add(
            TestUtils.create_attribute("Title", "Cells of the adult human heart"))
        bio_study_section.attributes.add(
            TestUtils.create_attribute("Description",
                                       "Cardiovascular disease is the leading cause of death worldwide."))
        bio_study_section.attributes.add(
            TestUtils.create_attribute("Organism", "Homo sapiens (human)"))
        bio_study_section.attributes.add(
            TestUtils.create_attribute("alias", "Phoenix-test-1"))

        bio_study_section.links.add(
            TestUtils.create_bio_study_link("ABC123", {TestUtils.create_attribute("alias", "Phoenix-test-1")}))
        bio_study_section.links.add(
            TestUtils.create_bio_study_link("SAMEA7249626", {TestUtils.create_attribute("Type", "BioSample")}))

        bio_study_section.subsections.add(
            TestUtils.create_sub_section("Author", {TestUtils.create_attribute("Name", "John Doe")}))

        bio_study.section = bio_study_section

        return bio_study

    @staticmethod
    def create_attribute(name, value):
        bio_study_attribute = BioStudiesAttribute()
        bio_study_attribute.name = name
        bio_study_attribute.value = value

        return bio_study_attribute

    @staticmethod
    def create_bio_study_link(url, bio_studies_attributes):
        bio_study_link = BioStudyLink()
        bio_study_link.url = url
        bio_study_link.attributes = bio_studies_attributes

        return bio_study_link

    @staticmethod
    def create_bio_study_file(path, file_type, bio_studies_attributes):
        bio_study_file = BioStudyFile()
        bio_study_file.path = path
        bio_study_file.file_type = file_type
        bio_study_file.attributes = bio_studies_attributes

        return bio_study_file

    @staticmethod
    def create_sub_section(section_type, biostudies_attributes):
        bio_study_subsection = BioStudySubsection()
        bio_study_subsection.type = section_type
        bio_study_subsection.attributes = biostudies_attributes

        return bio_study_subsection
