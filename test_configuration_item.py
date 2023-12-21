from main import (
    ConfigurationItem,
    ProjectManConfigTypeInvalidError,
    CONFIGURATION_ITEM_ACCEPTED_TYPES,
)
import pytest


get_conf_item = ConfigurationItem(
    item_type="issues",
    labels=["bug"],
    assignees=["thepetk"],
    milestones=["12/12/2023"],
    last_updated_on="2023-11-11T01:59:59",
    created_on="2023-11-10T01:59:59",
    closed_on="2023-11-12T01:59:59",
    reviewers=None,
)


def test_get_configuration_item_type_success():
    for item_type in CONFIGURATION_ITEM_ACCEPTED_TYPES:
        assert get_conf_item._get_configuration_item_type(item_type) == item_type


def test_get_configuration_item_type_failure():
    item_type = "Issues"
    with pytest.raises(ProjectManConfigTypeInvalidError):
        get_conf_item._get_configuration_item_type(item_type)


def test_split_filters_success():
    items_list = ["one", "!two"]
    inl = []
    exl = []
    for items in items_list:
        if items.startswith("!"):
            exl.append(items)
        else:
            inl.append(items)
        assert get_conf_item._split_filters(items)
