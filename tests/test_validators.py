import pytest

from exceptions import ProjectManValidationError
from mockers import ConfigurationMocker
from utils import ALL, CONFIGURATION_ITEM_ACCEPTED_TYPES, ISSUES, PULL_REQUESTS
from validators import FieldValidator

field_validator = FieldValidator()
mocker = ConfigurationMocker(
    labels=["bug"],
    assignees=["someone", "!another"],
    reviewers=["reviewer", "!noreviewer"],
    milestones=["important", "!unimportant"],
)

# ------------------ FieldValidator test cases -------------------- #


def test_field_validator_validate_success():
    values = [ISSUES, PULL_REQUESTS]
    field_validator.is_one_of = CONFIGURATION_ITEM_ACCEPTED_TYPES
    field_validator.default = ALL
    for value in values:
        mocker.config_dict["type"] = value
        assert (
            field_validator.validate("type", mocker.config_dict["type"])
            == mocker.config_dict["type"]
        )
    mocker.config_dict["type"] = "None"
    assert field_validator.validate("type", mocker.config_dict["type"]) == ALL

    field_validator.is_one_of = None
    field_validator.default = None
    for key in mocker.config_dict.keys():
        field_validator.is_instance = type(mocker.config_dict[key])
        assert (
            field_validator.validate(key, mocker.config_dict[key])
            == mocker.config_dict[key]
        )
    mocker.config_dict["closed_on"] = None
    assert (
        field_validator.validate("closed_on", mocker.config_dict["closed_on"]) is None
    )


def test_field_validator_validate_failure():
    field_validator.is_one_of = None
    field_validator.is_instance = list
    for value, optional in [("bvc", True), (None, False)]:
        field_validator.optional = optional
        with pytest.raises(ProjectManValidationError):
            field_validator.validate("labels", value)


# ----------------------------------------------------------------- #
