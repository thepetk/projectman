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
}

values = ["issues", "pull_requests"]


def test_field_validator_validate_success():
    for value in values:
        json_dict["type"] = value
        json_dict.validate(json_dict, "type") == json_dict["type"]
    json_dict["type"] = "None"
    assert field_validator.validate(json_dict, "type") == "all"

    for key in json_dict.keys():
        assert field_validator.validate(json_dict, key) == json_dict[key]


# optional
def test_field_validator_validate_failure():
    pass
