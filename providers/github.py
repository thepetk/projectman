from typing import Any

import github
from github.Repository import Repository

from configuration import ConfigurationFile, ConfigurationProject
from exceptions import GithubGraphQLQueryError, GithubObjectNotFoundError
from utils import GITHUB_TOKEN, REPO_NAME, Base, logger, now


class GithubProvider(Base):
    """
    GithubProvider is the class wrapping the PyGithub
    dependency and using its functionality in order to
    apply all actions needed in order to fetch, update,
    create github projects according to the given
    configuration.
    """

    def __init__(self) -> None:
        self.github = self._authenticate()

    def _authenticate(self) -> github.Github:
        _token = github.Auth.Token(GITHUB_TOKEN)
        return github.Github(auth=_token)

    def _get_repo(self, _repo_name=REPO_NAME) -> Repository:
        logger.debug(
            "%s::DEBUG::<%s>::getting repo %s" % (now(), self.class_name, _repo_name)
        )
        return self.github.get_repo(_repo_name)

    def _get_project_id(self, config_project: ConfigurationProject) -> str | None:
        _r = self._graphql_query(
            GraphQLQuery.get_project % (self.github.get_user().login)
        )
        for node in _r["data"]["user"]["projectsV2"]["nodes"]:
            if config_project.name == node["title"]:
                logger.debug(
                    "%s::DEBUG::<%s>::found id %s for project %s"
                    % (now(), self.class_name, node["id"], config_project.name)
                )
                return node["id"]
            logger.debug(
                "%s::DEBUG::<%s>::project %s not found"
                % (now(), self.class_name, config_project.name)
            )
        return None

    def _get_file_contents(self, _repo: Repository, filepath: str) -> str:
        logger.debug(
            "%s::DEBUG::<%s>::getting contents for %s"
            % (now(), self.class_name, filepath)
        )
        return _repo.get_contents(filepath).decoded_content.decode()

    def create_or_update_project(self, config_project: ConfigurationProject):
        _pid = self._get_project_id(config_project)
        if _pid is None:
            logger.debug(
                "%s::DEBUG::<%s>::creating project %s"
                % (now(), self.class_name, config_project.name)
            )
            _r = self._graphql_query(
                GraphQLQuery.create_project
                % (self._graphql_get_ownerId(), config_project.name)
            )
            _pid = _r["data"]["createProjectV2"]["projectV2"]["id"]

        logger.debug(
            "%s::DEBUG::<%s>::updating project %s - pid: %s"
            % (now(), self.class_name, config_project.name, _pid)
        )
        _r = self._graphql_query(
            GraphQLQuery.update_project
            % (
                _pid,
                config_project.name,
                str(config_project.public).lower(),
                config_project.description,
            )
        )
        self._update_issues(config_project)
        # self._update_pull_requests()

    def _update_issues(self, config_project: ConfigurationProject):
        repo = self._get_repo()
        issues = repo.get_issues()
        for issue in issues:
            # labels
            if (
                not config_project.issues.skip_labels
                and not config_project.issues.has_labels
            ):
                self._add_to_project(issue)
                continue

            labels = issue.get_labels()
            has_skipped_label = False

            for config_label in config_project.issues.skip_labels:
                if config_label in labels:
                    has_skipped_label = True
                    break
            if has_skipped_label:
                continue

            for config_label in config_project.issues.has_labels:
                if config_label in labels:
                    self._add_to_project(issue)
                    break
            # assignees
            if (
                not config_project.issues.skip_assignees
                and not config_project.issues.has_assignees
            ):
                self._add_to_project(issue)
                continue

            assignees = issue.get_assignees()
            has_skipped_assignees = False

            for config_assignes in config_project.issues.skip_assignees:
                if config_assignees in assignees:
                    has_skipped_assignees = True
                    break
            if has_skipped_assignees:
                continue

            for config_assignees in config_project.issues.has_assignees:
                if config_assignees in assignees:
                    self._add_to_project(issue)
                    break

            # reviewers
            if (
                not config_project.issues.skip_reviewers
                and not config_project.issues.has_reviewers
            ):
                self._add_to_project(issue)
                continue

            reviewers = issue.get_reviewers()
            has_skipped_reviewers = False

            for config_reviewers in config_project.issues.skip_reviewers:
                if config_reviewers in reviewers:
                    has_skipped_reviewers = True
                    break
            if has_skipped_reviewers:
                continue

            for config_reviewers in config_project.issues.has_reviewers:
                if config_reviewers in reviewers:
                    self._add_to_project(issue)
                    break
            # milestones
            if (
                not config_project.issues.skip_milestones
                and not config_project.issues.has_milestones
            ):
                self._add_to_project(issue)
                continue

            milestones = issue.get_milestones()
            has_skipped_milestones = False

            for config_milestones in config_project.issues.skip_milestones:
                if config_milestones in milestones:
                    has_skipped_milestones = True
                    break
            if has_skipped_milestones:
                continue

            for config_milestones in config_project.issues.has_milestones:
                if config_milestones in milestones:
                    self._add_to_project(issue)
                    break
            # last_updated_on
            last_updated_on = issue.get_last_updated_on()
            for config_last_updated_on in config_project.issues.last_updated_on:
                if config_last_updated_on in last_updated_on:
                    self._add_to_project(issue)
                    break

    def _add_to_project(self, issue):
        print(issue.get_labels())

    def _update_pull_requests():
        return

    def _graphql_query(self, query: str) -> dict[str, Any]:
        _, data = self.github.get_user()._requester.requestJsonAndCheck(
            "POST", "https://api.github.com/graphql", input={"query": query}
        )
        if "errors" in data:
            errmsg = "errors:: "
            for err in data["errors"]:
                errmsg += "{}, ".format(err["message"])
            raise GithubGraphQLQueryError(errmsg)
        return data

    def _graphql_get_ownerId(self) -> str:
        _r = self._graphql_query(
            GraphQLQuery.get_owner % (self.github.get_user().login)
        )
        return _r["data"]["repositoryOwner"]["id"]

    def get_configuration_file(self, filepath: str) -> ConfigurationFile:
        """
        Gets the content (string) from a given filepath
        inside a github repo and transforms it into a
        ConfigurationFile type object.

        :raises: GithubObjectNotFoundError
        """
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
        return ConfigurationFile(content=_content, filepath=filepath)


class GraphQLQuery:
    get_project: str = """
        query{
            user(login: "%s"){
                projectsV2(first: 100) {
                    nodes {
                        id,
                        title
                    }
                }
            }
        }
        """
    get_owner: str = """
        query{
            repositoryOwner(login: "%s"){
                id
                login
                repositories(first:1) {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
        }
        """
    create_project: str = """
        mutation {
            createProjectV2(input: {ownerId: "%s", title: "%s"}) {
                projectV2 { id }
            }
        }
        """

    update_project: str = """
        mutation {
            updateProjectV2(input: {projectId: "%s", title: "%s", public: %s, shortDescription: "%s"}) {
                projectV2 { id }
            }
        }
        """  # noqa: E501
