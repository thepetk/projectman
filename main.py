import json
import os
from typing import Any, Optional

import github
from github.Repository import Repository

from mocker import GithubMocker

# Typing items
CONFIGURATION_VALUE = Optional[str | list[str] | bool]
CONFIGURATION_DICT = dict[str, CONFIGURATION_VALUE]
SPLITTED_FILTERS = tuple[list[str], list[str]]

# Script environment variables
ENV = os.getenv("PROJECTMAN_ENV", "prod")
TEST_ENV = "test"


def _is_test_env():
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


class ProjectManConfigTypeInvalidError(Exception):
    pass


class FieldNotInConfigurationFieldsError(Exception):
    pass


class FieldValidatorNotExistsError(Exception):
    pass


class ProjectManValidationError(Exception):
    pass


class ProjectManInvalidJsonFileError(Exception):
    pass


class GithubObjectNotFoundError(Exception):
    pass


class Base:
    @property
    def class_name(self) -> str:
        return self.__class__.__name__


class FieldValidator(Base):
    def __init__(
        self,
        is_one_of: Optional[list[str]] = None,
        is_instance: Any = None,
        default: Optional[str] = None,
        optional: bool = True,
    ) -> None:
        self.is_one_of = is_one_of
        self.is_instance = is_instance
        self.default = default
        self.optional = optional

    def validate(self, key: str, value: CONFIGURATION_VALUE) -> CONFIGURATION_VALUE:
        if self.is_one_of is not None:
            return value if value in self.is_one_of else self.default
        elif self.is_instance is not None:
            if isinstance(value, self.is_instance):
                return value
            elif value is None and self.default is not None:
                return self.default
            elif value is None and self.optional is True:
                return value
            else:
                raise ProjectManValidationError(
                    f"error: invalid type. Key {key} of type {self.is_instance} has type {type(value)}"  # noqa: E501
                )
        else:
            return value


# Optional and Required fields inside .projectman.json
CONFIGURATION_FIELDS = {
    "name": FieldValidator(is_instance=str, default="ProjectMan Project"),
    "labels": FieldValidator(is_instance=list, default=[]),
    "assignees": FieldValidator(is_instance=list, default=[]),
    "reviewers": FieldValidator(is_instance=list, default=[]),
    "milestones": FieldValidator(is_instance=list, default=[]),
    "created_on": FieldValidator(is_instance=str, default=""),
    "last_updated_on": FieldValidator(is_instance=str, default=""),
    "closed_on": FieldValidator(is_instance=str, default=""),
    "type": FieldValidator(is_one_of=CONFIGURATION_ITEM_ACCEPTED_TYPES, default=ALL),
}


class ConfigurationFile(Base):
    def __init__(self, content: str, filepath: str) -> None:
        self.content = content
        self.filepath = filepath


class GithubProvider(Base):
    def __init__(self) -> None:
        self.github = self._authenticate()

    def _authenticate(self) -> github.Github:
        if _is_test_env():
            return github.Github(auth=None)
        _token = github.Auth.Token(GITHUB_TOKEN)
        return github.Github(auth=_token)

    def _get_repo(self, _repo_name=REPO_NAME) -> Repository:
        if _is_test_env():
            return GithubMocker.REPO
        return self.github.get_repo(_repo_name)

    def _get_file_contents(self, _repo: Repository, filepath: str) -> str:
        if _is_test_env():
            return GithubMocker.SIMPLE_CONTENT
        return _repo.get_contents(filepath).decoded_content.decode()

    def _create_or_update_project(self, _attrs: CONFIGURATION_DICT):
        return self.github.get_user().create_project(name=_attrs["name"])

    def get_file_contents(self, filepath: str) -> str:
        try:
            _repo = self._get_repo(REPO_NAME)
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: bad creds or repository {REPO_NAME} not found"  # noqa: E501
            )
        try:
            _content = self._get_file_contents(_repo, filepath)
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: file {filepath} not found"
            )
        return _content


class ConfigurationItem(Base):
    def __init__(
        self,
        name: str,
        item_type: str,
        labels: list[str],
        assignees: list[str],
        milestones: list[str],
        last_updated_on: str,
        created_on: str,
        closed_on: str,
        reviewers: list[str] = [],
    ) -> None:
        self.name = name
        self.item_type = self._get_configuration_item_type(item_type)
        self.has_labels, self.skip_labels = self._split_filters(labels)
        self.has_assignees, self.skip_assignees = self._split_filters(assignees)
        self.has_reviewers, self.skip_reviewers = self._split_filters(reviewers)
        self.has_milestones, self.skip_milestones = self._split_filters(milestones)
        self.last_updated_on = last_updated_on
        self.created_on = created_on
        self.closed_on = closed_on

    def _get_configuration_item_type(self, item_type: str) -> str:
        if item_type in CONFIGURATION_ITEM_ACCEPTED_TYPES:
            return item_type
        else:
            raise ProjectManConfigTypeInvalidError(
                f"{self.class_name}:: error: type {item_type} not in CONFIGURATION_ITEM_ACCEPTED_TYPES"  # noqa: E501
            )

    def _split_filters(self, items_list: list[str]) -> SPLITTED_FILTERS:
        inlist = []
        exlist = []

        for i in items_list:
            if i.startswith("!"):
                exlist.append(i.replace("!", ""))
            else:
                inlist.append(i)
        return inlist, exlist


class ConfigurationProject(Base):
    def __init__(
        self,
        issues_item: Optional[list[ConfigurationItem]] = None,
        pull_requests: Optional[list[ConfigurationItem]] = None,
    ) -> None:
        self.issues = issues_item
        self.pull_requests = pull_requests


class Configuration(Base):
    def __init__(self, projects: list[ConfigurationProject]) -> None:
        self.projects = projects


class ConfigurationManager(Base):
    def __init__(self) -> None:
        self.json_parser = JsonParser()
        self.github_provider = GithubProvider()

    def _get_config_file(self, filepath=PROJECTMAN_FILEPATH) -> ConfigurationFile:
        return ConfigurationFile(
            content=self.github_provider.get_file_contents(filepath), filepath=filepath
        )

    @property
    def _parsed_list(self) -> list[CONFIGURATION_DICT]:
        return self.json_parser.parse(self._get_config_file())

    def _create_config_item(
        self, item_type: str, project_dict: CONFIGURATION_DICT
    ) -> ConfigurationItem:
        return ConfigurationItem(
            item_type=item_type,
            name=project_dict.get("name"),
            labels=project_dict.get("labels"),
            assignees=project_dict.get("assignees"),
            milestones=project_dict.get("milestones"),
            last_updated_on=project_dict.get("last_updated_on"),
            created_on=project_dict.get("created_on"),
            closed_on=project_dict.get("closed_on"),
        )

    def generate_configuration(self) -> Configuration:
        _config_projects = []
        for project_dict in self._parsed_list:
            configuration_project = ConfigurationProject()
            if project_dict.get("type") in [ISSUES, ALL]:
                configuration_project.issues = self._create_config_item(
                    ISSUES, project_dict
                )
            if project_dict.get("type") in [PULL_REQUESTS, ALL]:
                configuration_project.pull_requests = self._create_config_item(
                    PULL_REQUESTS, project_dict
                )
            if (
                configuration_project.issues is None
                or configuration_project.pull_requests is None
            ):
                continue

            _config_projects.append(configuration_project)

        return Configuration(projects=_config_projects)


class JsonParser(Base):
    def _getkey(
        self,
        json_dict: CONFIGURATION_DICT,
        key: CONFIGURATION_VALUE,
    ) -> CONFIGURATION_VALUE:
        if key not in CONFIGURATION_FIELDS.keys():
            raise FieldNotInConfigurationFieldsError(
                f"error: invalid field. Field {key} is not a valid configuration field"
            )
        if not isinstance(CONFIGURATION_FIELDS.get(key), FieldValidator):
            raise FieldValidatorNotExistsError(
                f"error: no field validator defined for key {key}"
            )
        return CONFIGURATION_FIELDS[key].validate(key, json_dict.get(key))

    def parse(self, config_file: ConfigurationFile) -> list[CONFIGURATION_DICT]:
        parsed_list = []
        try:
            json_dict_list = json.loads(config_file.content)
        except json.decoder.JSONDecodeError:
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {config_file.filepath} is invalid"
            )

        if not isinstance(json_dict_list, list):
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {config_file.filepath} is not a list"
            )
        for json_dict in json_dict_list:
            parsed_list.append(
                {
                    key: self._getkey(json_dict, key)
                    for key in CONFIGURATION_FIELDS.keys()
                }
            )
        return parsed_list


def main():
    configuration_manager = ConfigurationManager()
    _ = configuration_manager.generate_configuration()


if __name__ == "__main__":
    main()
