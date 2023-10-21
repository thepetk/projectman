import json
import os
import github


PROJECTMAN_FILEPATH = ".projectman.json"

REPO_NAME = os.getenv("REPO")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


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

    def get_configuration_file(self, filepath = PROJECTMAN_FILEPATH):
        try:
            _r = self.github.get_repo(REPO_NAME)
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: repository {REPO_NAME} not found"
            )
        try:
            _c = _r.get_contents(filepath).decoded_content
        except github.GithubException:
            raise GithubObjectNotFoundError(
                f"{self.class_name}:: error: file {filepath} not found"
            )
        return ConfigurationFile(content=_c, filepath=filepath)


class Configuration(Base):
    def __init__(self):
        # TODO: Add attributes for project configuration
        pass

class JsonParser(Base):
    def _getkey(self, json_dict, key):
        # TODO: Make a better validation method
        if key in ["issue"] and json_dict.get(key) is None:
            raise Exception()
        else:
            return json_dict.get(key)

    def parse(self, config_file):
        config_file = open(".projectman.json")
        try:
            json_dict = json.load(config_file.content)
        except json.decoder.JSONDecodeError:
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {config_file.filepath} is invalid"
            )
        # TODO: Return a proper configuration object
        return json_dict


def main():
    github_provider = GithubProvider()
    config_file = github_provider.get_configuration_file()
    parser = JsonParser()
    # TODO: Finalize script
    _ = parser.parse(config_file)



if __name__ == "__main__":
    main()
