from typing import Optional

from utils import ALL, CONFIGURATION_DICT, ISSUES, PULL_REQUESTS, SPLITTED_FILTERS, Base


class ConfigurationFile(Base):
    def __init__(self, content: str, filepath: str) -> None:
        self.content = content
        self.filepath = filepath


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
        self.item_type = item_type
        self.has_labels, self.skip_labels = self._split_filters(labels)
        self.has_assignees, self.skip_assignees = self._split_filters(assignees)
        self.has_reviewers, self.skip_reviewers = self._split_filters(reviewers)
        self.has_milestones, self.skip_milestones = self._split_filters(milestones)
        self.last_updated_on = last_updated_on
        self.created_on = created_on
        self.closed_on = closed_on

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
        name: str,
        description: str,
        issues: Optional[list[ConfigurationItem]] = None,
        pull_requests: Optional[list[ConfigurationItem]] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.issues = issues
        self.pull_requests = pull_requests


class Configuration(Base):
    def __init__(self, projects: list[ConfigurationProject]) -> None:
        self.projects = projects


class ConfigurationManager(Base):
    def __init__(self, parsed_list: list[CONFIGURATION_DICT]) -> None:
        self.parsed_list = parsed_list

    def _create_config_item(
        self, item_type: str, project_dict: CONFIGURATION_DICT
    ) -> ConfigurationItem:
        return ConfigurationItem(
            item_type=item_type,
            labels=project_dict.get("labels"),
            assignees=project_dict.get("assignees"),
            milestones=project_dict.get("milestones"),
            last_updated_on=project_dict.get("last_updated_on"),
            created_on=project_dict.get("created_on"),
            closed_on=project_dict.get("closed_on"),
        )

    def generate_configuration(
        self, parsed_list: list[CONFIGURATION_DICT]
    ) -> Configuration:
        _config_projects = []
        for project_dict in parsed_list:
            configuration_project = ConfigurationProject(name=project_dict.get("name"))
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
                and configuration_project.pull_requests is None
            ):
                continue

            _config_projects.append(configuration_project)

        return Configuration(projects=_config_projects)
