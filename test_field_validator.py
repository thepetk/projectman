from main import FieldValidator, ProjectManValidationError
import pytest


field_validator = FieldValidator()
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
values = ["issues", "pull_requests"]


def test_field_validator_validate_success():
    for value in values:
        if json_dict.get("type") in values:
            assert field_validator.validate(json_dict, "type") == json_dict["type"]
        elif json_dict.get("type") == None and json_dict.get("type") not in values:
            assert field_validator.validate(json_dict, "type") == "all"

    for key in json_dict:
        if key == isinstance(json_dict.get(value), type(value)):
            assert field_validator.validate(json_dict, "type") == json_dict["type"]


def test_field_validator_validate_failure():
    pass
