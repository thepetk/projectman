# Typing Items
import os
from typing import Optional

CONFIGURATION_VALUE = Optional[str | list[str] | bool]
CONFIGURATION_DICT = dict[str, CONFIGURATION_VALUE]
SPLITTED_FILTERS = tuple[list[str], list[str]]

# Project Configuration
PULL_REQUESTS = "pull_requests"
ISSUES = "issues"
ALL = "all"
CONFIGURATION_ITEM_ACCEPTED_TYPES = [PULL_REQUESTS, ISSUES, ALL]

# .projectman.json configuration variables
PROJECTMAN_FILEPATH = ".projectman.json"
REPO_NAME = os.getenv("REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class Base:
    """
    Base is the base class for all classes used
    inside the projectman repo. As a result every
    class inherrits some necessary attributes.
    """

    @property
    def class_name(self) -> str:
        return self.__class__.__name__
