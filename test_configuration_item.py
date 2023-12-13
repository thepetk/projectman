from main import ConfigurationItem, ProjectManConfigTypeInvalidError
import pytest

items = ["issues", "prs", "all"]

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


def test_get_configuration_item_success():
    for item_type in items:
        if item_type == "issues":
            assert get_conf_item._get_configuration_item_type(item_type) == "issues"


def test_get_configuration_item_failure():
    pass


def test_split_filters_success():
    pass
