import json
import os
import github

REQUIRED_FIELDS = {"issues": list}
OPTIONAL_FIELDS = {"labels": list, "prs": list}
PROJECTMAN_FILEPATH = ".projectman.json"

REPO_NAME = os.getenv("REPO")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class ProjectManValidationError(Exception):
    pass


class ProjectManFileNotFoundError(Exception):
    pass


class ProjectManInvalidJsonFileError(Exception):
    pass


class GithubObjectNotFoundError(Exception):
    pass


class Base:
    @property
    def class_name(self):
        return self.__class__.__name__


class ConfigurationFile(Base):
    def __init__(self, content, filepath):
        self.content = content
        self.filepath = filepath


class GithubProvider(Base):
    def __init__(self):
        self.github = self._authenticate()

    def _authenticate(self):
        _token = github.Auth.Token(GITHUB_TOKEN)
        return github.Github(auth=_token)

    def get_configuration_file(self, filepath=PROJECTMAN_FILEPATH):
        try:
            _r = self.github.get_repo(REPO_NAME)
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: repository {REPO_NAME} not found"
            )
        try:
            _c = _r.get_contents(filepath).decoded_content.decode()
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: file {filepath} not found"
            )
        return ConfigurationFile(content=_c, filepath=filepath)


class Configuration(Base):
    def __init__(self, labels, issues, pull_requests):
        self.labels = labels
        self.issues = issues
        self.pull_requests = pull_requests
        # TODO: Add attributes for project configuration


class JsonParser(Base):
    def _getkey(self, json_dict, key):
        if key in REQUIRED_FIELDS.keys() and json_dict.get(key) is None:
            raise ProjectManValidationError(
                f"{self.class_name}:: error: required key {key} is missing"
            )
        elif REQUIRED_FIELDS.get(key) and not isinstance(
            json_dict.get(key), REQUIRED_FIELDS.get(key)
        ):
            raise Exception(
                f"error: invalid type. Key {key} of type {REQUIRED_FIELDS.get(key)} has type {type(json_dict.get(key))}"
            )

        else:
            return json_dict.get(key)

    def parse(self, config_file):
        try:
            json_dict = json.loads(config_file.content)

        except json.decoder.JSONDecodeError:
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {config_file.filepath} is invalid"
            )
        # TODO: Return a proper configuration object

        return


def main():
    github_provider = GithubProvider()
    config_file = github_provider.get_configuration_file()
    parser = JsonParser()

    # TODO: Finalize script

    _ = parser.parse(config_file)


if __name__ == "__main__":
    main()
