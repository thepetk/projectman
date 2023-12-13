import pytest

from main import (
    ConfigurationFile,
    FieldNotInConfigurationFieldsError,
    JsonParser,
    ProjectManInvalidJsonFileError,
)

json_parser = JsonParser()
filepath = "filepath"


def test_json_parser_get_key_success():
    json_dict = {
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
            assert json_parser._getkey(json_dict, key) == "all"
        else:
            assert json_parser._getkey(json_dict, key) == json_dict[key]

    for value in ["issues", "pull_requests"]:
        json_dict["type"] = value
        assert json_parser._getkey(json_dict, "type") == json_dict["type"]


def test_json_parser_get_key_failure_invalid_type():
    key = "None"
    json_dict = {key: "kok"}

    with pytest.raises(FieldNotInConfigurationFieldsError):
        json_parser._getkey(json_dict, key)


def test_json_parser_parse_success():
    content = '[{"labels": ["bug"],"assignees": ["thepetk"],"reviewers": ["thepetk"],"milestones": ["12/12/2023"],"created_on": "dmdmd","last_updated_on": "fefde","closed_on": "rfcrsd","type": "None"}]'  # noqa: E501
    expected_result = [
        {
            "labels": ["bug"],
            "assignees": ["thepetk"],
            "reviewers": ["thepetk"],
            "milestones": ["12/12/2023"],
            "created_on": "dmdmd",
            "last_updated_on": "fefde",
            "closed_on": "rfcrsd",
            "type": "all",
        }
    ]
    config_file = ConfigurationFile(content=content, filepath=filepath)
    assert json_parser.parse(config_file) == expected_result


def test_json_parser_parse_failure():
    wrong_decoded_content = "{'test':'test'}"
    no_list_content = '{"labels": ["bug"],"assignees": ["thepetk"],"reviewers": ["thepetk"],"milestones": ["12/12/2023"],"created_on": "dmdmd","last_updated_on": "fefde","closed_on": "rfcrsd","type": "None"}'  # noqa: E501

    config_file = ConfigurationFile(content=wrong_decoded_content, filepath=filepath)
    with pytest.raises(ProjectManInvalidJsonFileError):
        json_parser.parse(config_file)

    config_file = ConfigurationFile(content=no_list_content, filepath=filepath)
    with pytest.raises(ProjectManInvalidJsonFileError):
        json_parser.parse(config_file)
