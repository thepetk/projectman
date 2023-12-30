import github
from github.Repository import Repository

from configuration import ConfigurationProject
from exceptions import GithubObjectNotFoundError
from mockers import GithubMocker
from utils import GITHUB_TOKEN, REPO_NAME, Base, is_test_env

mocker = GithubMocker()


class GithubProvider(Base):
    def __init__(self) -> None:
        self.github = self._authenticate()

    def _authenticate(self) -> github.Github:
        if is_test_env():
            return github.Github(auth=None)
        _token = github.Auth.Token(GITHUB_TOKEN)
        return github.Github(auth=_token)

    def _get_repo(self, _repo_name=REPO_NAME) -> Repository:
        if is_test_env():
            return GithubMocker.repo
        return self.github.get_repo(_repo_name)

    def _get_file_contents(self, _repo: Repository, filepath: str) -> str:
        if is_test_env():
            return GithubMocker.file_contents
        return _repo.get_contents(filepath).decoded_content.decode()

    def create_or_update_project(self, config_project: ConfigurationProject):
        return self.github.get_user().create_project(
            name=config_project.name, body=config_project.description
        )

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
