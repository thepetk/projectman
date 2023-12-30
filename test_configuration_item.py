import pytest

from exceptions import ProjectManConfigTypeInvalidError
from mockers import ConfigurationMocker
from utils import CONFIGURATION_ITEM_ACCEPTED_TYPES

mocker = ConfigurationMocker(
    labels=["bug"],
    assignees=["someone", "!another"],
    reviewers=["reviewer", "!noreviewer"],
    milestones=["important", "!unimportant"],
)
config_item = mocker.configuration_item


def test_get_configuration_item_type_success():
    for item_type in CONFIGURATION_ITEM_ACCEPTED_TYPES:
        assert config_item._get_configuration_item_type(item_type) == item_type


def test_get_configuration_item_type_failure():
    item_type = "labels"
    with pytest.raises(ProjectManConfigTypeInvalidError):
        config_item._get_configuration_item_type(item_type)


def test_split_filters_success():
    items_list = ["one", "!two"]
    inl = ["one"]
    exl = ["two"]
    assert (inl, exl) == config_item._split_filters(items_list)
