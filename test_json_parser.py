import pytest

from main import (
    ALL,
    ISSUES,
    PULL_REQUESTS,
    ConfigurationFile,
    FieldNotInConfigurationFieldsError,
    JsonParser,
    ProjectManInvalidJsonFileError,
)
from mocker import GithubMocker

json_parser = JsonParser()


def test_json_parser_get_key_success():
    json_dict = {
        "name": "test",
        "labels": ["bug"],
        "assignees": ["thepetk"],
        "reviewers": ["thepetk"],
        "milestones": ["12/12/2023"],
        "created_on": "dmdmd",
        "last_updated_on": "fefde",
        "closed_on": "rfcrsd",
        "type": "None",
    }
    keys = [
        "name",
        "labels",
        "assignees",
        "reviewers",
        "milestones",
        "created_on",
        "last_updated_on",
        "closed_on",
        "type",
    ]

    for key in keys:
        if key == "type":
            assert json_parser._getkey(json_dict, key) == ALL
        else:
            assert json_parser._getkey(json_dict, key) == json_dict[key]

    for value in [ISSUES, PULL_REQUESTS]:
        json_dict["type"] = value
        assert json_parser._getkey(json_dict, "type") == json_dict["type"]


def test_json_parser_get_key_failure_invalid_type():
    key = "None"
    json_dict = {key: "kok"}

    with pytest.raises(FieldNotInConfigurationFieldsError):
        json_parser._getkey(json_dict, key)


def test_json_parser_parse_success():
    expected_result = [
        {
            "name": "test",
            "labels": ["bug"],
            "assignees": ["thepetk"],
            "reviewers": ["thepetk"],
            "milestones": ["12/12/2023"],
            "created_on": "dmdmd",
            "last_updated_on": "fefde",
            "closed_on": "rfcrsd",
            "type": ALL,
        }
    ]
    config_file = ConfigurationFile(
        content=GithubMocker.SIMPLE_CONTENT, filepath=GithubMocker.FILEPATH
    )
    assert json_parser.parse(config_file) == expected_result


def test_json_parser_parse_failure():
    wrong_decoded_content = "{'test':'test'}"

    config_file = ConfigurationFile(
        content=wrong_decoded_content, filepath=GithubMocker.FILEPATH
    )
    with pytest.raises(ProjectManInvalidJsonFileError):
        json_parser.parse(config_file)

    config_file = ConfigurationFile(
        content=GithubMocker.NO_LIST_CONTENT, filepath=GithubMocker.FILEPATH
    )
    with pytest.raises(ProjectManInvalidJsonFileError):
        json_parser.parse(config_file)
