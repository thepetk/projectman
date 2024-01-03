from mockers import ConfigurationMocker

mocker = ConfigurationMocker(
    labels=["bug"],
    assignees=["someone", "!another"],
    reviewers=["reviewer", "!noreviewer"],
    milestones=["important", "!unimportant"],
)
config_item = mocker.configuration_item


# ----------------- ConfigurationItem test cases ------------------ #


def test_split_filters_success():
    items_list = ["one", "!two"]
    inl = ["one"]
    exl = ["two"]
    assert (inl, exl) == config_item._split_filters(items_list)


# ----------------------------------------------------------------- #

# TODO: Add ConfigurationManager test cases
