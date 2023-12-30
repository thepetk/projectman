from configuration import ConfigurationFile, ConfigurationManager
from parsers import JsonParser
from providers import GithubProvider
from utils import PROJECTMAN_FILEPATH


def main():
    provider = GithubProvider()
    parser = JsonParser()
    file_contents = provider.get_file_contents(PROJECTMAN_FILEPATH)
    config_file = ConfigurationFile(content=file_contents, filepath=PROJECTMAN_FILEPATH)
    parsed_list = parser.parse(config_file)
    configuration_manager = ConfigurationManager(parsed_list=parsed_list)
    configuration = configuration_manager.generate_configuration()
    for project in configuration.projects:
        provider.create_or_update_project(project)


if __name__ == "__main__":
    main()
