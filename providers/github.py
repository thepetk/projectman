import github
from github.Repository import Repository

from configuration import ConfigurationFile
from exceptions import GithubObjectNotFoundError
from utils import GITHUB_TOKEN, REPO_NAME, Base


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
        return self.github.get_repo(_repo_name)

    def _get_file_contents(self, _repo: Repository, filepath: str) -> str:
        return _repo.get_contents(filepath).decoded_content.decode()

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
