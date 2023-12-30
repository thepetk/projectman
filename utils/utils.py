# Typing Items
import os
from typing import Optional

CONFIGURATION_VALUE = Optional[str | list[str] | bool]
CONFIGURATION_DICT = dict[str, CONFIGURATION_VALUE]
SPLITTED_FILTERS = tuple[list[str], list[str]]

# Script environment variables
ENV = os.getenv("PROJECTMAN_ENV", "prod")
TEST_ENV = "test"


def is_test_env():
    return ENV == TEST_ENV


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
    @property
    def class_name(self) -> str:
        return self.__class__.__name__
