import json
import os
from typing import Any, Optional

import github

# Typing items
CONFIGURATION_VALUE = Optional[str | list[str] | bool]
SPLITTED_FILTERS = tuple[list[str], list[str]]

# Project Configuration
CONFIGURATION_ITEM_ACCEPTED_TYPES = ["issues", "prs", "all"]

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
    "labels": FieldValidator(is_instance=list),
    "assignees": FieldValidator(is_instance=list),
    "reviewers": FieldValidator(is_instance=list),
    "milestones": FieldValidator(is_instance=list),
    "created_on": FieldValidator(is_instance=str),
    "last_updated_on": FieldValidator(is_instance=str),
    "closed_on": FieldValidator(is_instance=str),
    "type": FieldValidator(is_one_of=CONFIGURATION_ITEM_ACCEPTED_TYPES, default="all"),
}


class ConfigurationFile(Base):
    def __init__(self, content: str, filepath: str) -> None:
        self.content = content
        self.filepath = filepath


class GithubProvider(Base):
    def __init__(self) -> None:
        self.github = self._authenticate()

    def _authenticate(self) -> github.Github:
        _token = github.Auth.Token(GITHUB_TOKEN)
        return github.Github(auth=_token)

    def get_configuration_file(
        self, filepath: str = PROJECTMAN_FILEPATH
    ) -> ConfigurationFile:
        try:
            _r = self.github.get_repo(REPO_NAME)
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: bad creds or repository {REPO_NAME} not found"  # noqa: E501
            )
        try:
            _c = _r.get_contents(filepath).decoded_content.decode()
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: file {filepath} not found"
            )
        return ConfigurationFile(content=_c, filepath=filepath)


class ConfigurationItem(Base):
    def __init__(
        self,
        item_type: str,
        labels: list[str],
        assignees: list[str],
        milestones: list[str],
        last_updated_on: str,
        created_on: str,
        closed_on: str,
        reviewers: list[str] = [],
    ) -> None:
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

    def generate_configuration(self) -> Configuration:
        config_file = self.github_provider.get_configuration_file()
        parsed_list = self.json_parser.parse(config_file)
        configuration_projects = []
        for project_dict in parsed_list:
            configuration_project = ConfigurationProject()
            if project_dict.get("type") in ["issues", "all"]:
                configuration_project.issues = ConfigurationItem(
                    item_type="issues",
                    labels=project_dict.get("labels"),
                    assignees=project_dict.get("assignees"),
                    milestones=project_dict.get("milestones"),
                    last_updated_on=project_dict.get("last_updated_on"),
                    created_on=project_dict.get("created_on"),
                    closed_on=project_dict.get("closed_on"),
                )
            if project_dict.get("type") in ["pull_requests", "all"]:
                configuration_project.pull_requests = ConfigurationItem(
                    item_type="pull_requests",
                    labels=project_dict.get("labels"),
                    assignees=project_dict.get("assignees"),
                    reviewers=project_dict.get("reviewers"),
                    milestones=project_dict.get("milestones"),
                    last_updated_on=project_dict.get("last_updated_on"),
                    created_on=project_dict.get("created_on"),
                    closed_on=project_dict.get("closed_on"),
                )
            if (
                configuration_project.issues is None
                or configuration_project.pull_requests is None
            ):
                continue

            configuration_projects.append(configuration_project)

        return Configuration(projects=configuration_projects)


class JsonParser(Base):
    def _getkey(
        self,
        json_dict: dict[str, CONFIGURATION_VALUE],
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

    def parse(
        self, config_file: ConfigurationFile
    ) -> list[dict[str, CONFIGURATION_VALUE]]:
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
