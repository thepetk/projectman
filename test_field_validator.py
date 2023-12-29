import pytest

from main import (
    ALL,
    CONFIGURATION_ITEM_ACCEPTED_TYPES,
    ISSUES,
    PULL_REQUESTS,
    FieldValidator,
    ProjectManValidationError,
)

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


def test_field_validator_validate_success():
    values = [ISSUES, PULL_REQUESTS]
    field_validator.is_one_of = CONFIGURATION_ITEM_ACCEPTED_TYPES
    field_validator.default = ALL
    for value in values:
        json_dict["type"] = value
        assert field_validator.validate("type", json_dict["type"]) == json_dict["type"]
    json_dict["type"] = "None"
    assert field_validator.validate("type", json_dict["type"]) == ALL

    field_validator.is_one_of = None
    field_validator.default = None
    for key in json_dict.keys():
        field_validator.is_instance = type(json_dict[key])
        assert field_validator.validate(key, json_dict[key]) == json_dict[key]
    json_dict["closed_on"] = None
    assert field_validator.validate("closed_on", json_dict["closed_on"]) is None


def test_field_validator_validate_failure():
    field_validator.is_one_of = None
    field_validator.is_instance = list
    for value, optional in [("bvc", True), (None, False)]:
        field_validator.optional = optional
        with pytest.raises(ProjectManValidationError):
            field_validator.validate("labels", value)
