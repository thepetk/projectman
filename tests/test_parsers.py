import pytest

from configuration import ConfigurationFile
from exceptions import (
    FieldNotInConfigurationFieldsError,
    ProjectManInvalidJsonFileError,
)
from mockers.mockers import ConfigurationMocker
from parsers import JsonParser
from utils import ALL, ISSUES, PULL_REQUESTS

json_parser = JsonParser()
mocker = ConfigurationMocker(
    item_type="all",
    labels=["bug"],
    assignees=["someone", "!another"],
    reviewers=["reviewer", "!noreviewer"],
    milestones=["important", "!unimportant"],
)


# --------------------- JSON Parser test cases -------------------- #


def test_json_parser_get_key_success():
    for key in mocker.config_dict.keys():
        if key == "type":
            assert json_parser._getkey(mocker.config_dict, key) == ALL
        else:
            assert (
                json_parser._getkey(mocker.config_dict, key) == mocker.config_dict[key]
            )

    for value in [ISSUES, PULL_REQUESTS]:
        mocker.config_dict["type"] = value
        assert (
            json_parser._getkey(mocker.config_dict, "type")
            == mocker.config_dict["type"]
        )


def test_json_parser_get_key_failure_invalid_type():
    key = "None"
    some_dict = {key: "key"}

    with pytest.raises(FieldNotInConfigurationFieldsError):
        json_parser._getkey(some_dict, key)


def test_json_parser_parse_success():
    expected_result = [
        {
            "assignees": ["someone", "!another"],
            "closed_on": "2023-11-11T01:59:59",
            "created_on": "2023-11-11T01:59:59",
            "description": "",
            "labels": ["bug"],
            "last_updated_on": "2023-11-11T01:59:59",
            "milestones": ["important", "!unimportant"],
            "name": "test",
            "type": "pull_requests",
            "reviewers": ["reviewer", "!noreviewer"],
        }
    ]
    config_file = ConfigurationFile(
        content=mocker.list_json_content, filepath=mocker.filepath
    )
    assert json_parser.parse(config_file) == expected_result


def test_json_parser_parse_failure():
    wrong_decoded_content = "{'test':'test'}"

    config_file = ConfigurationFile(
        content=wrong_decoded_content, filepath=mocker.filepath
    )
    with pytest.raises(ProjectManInvalidJsonFileError):
        json_parser.parse(config_file)

    config_file = ConfigurationFile(
        content=mocker.no_list_json_content, filepath=mocker.filepath
    )
    with pytest.raises(ProjectManInvalidJsonFileError):
        json_parser.parse(config_file)


# ----------------------------------------------------------------- #
