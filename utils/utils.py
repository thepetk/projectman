# Typing Items
import datetime
import logging
import logging.config
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


def now() -> str:
    return datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")


def get_logger() -> logging.StreamHandler:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logger = logging.getLogger("myLogger")
    return logger


logger = get_logger()


class Base:
    """
    Base is the base class for all classes used
    inside the projectman repo. As a result every
    class inherrits some necessary attributes.
    """

    @property
    def class_name(self) -> str:
        return self.__class__.__name__
