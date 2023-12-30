from configuration import ConfigurationFile, ConfigurationManager
from parsers import JsonParser
from providers import GithubProvider
from utils import PROJECTMAN_FILEPATH


def main():
    """
    The main method is handling the flow of execution for projectman.
    First creates a provider & a parser object in order to fetch info
    from the given repo. Finally, it upserts all projects with the help
    of the configuration manager.
    """
    provider, parser = GithubProvider(), JsonParser()
    # Transform projectman file into config object.
    file_contents = provider.get_file_contents(PROJECTMAN_FILEPATH)
    config_file = ConfigurationFile(content=file_contents, filepath=PROJECTMAN_FILEPATH)
    parsed_list = parser.parse(config_file)
    # Upsert all given projects
    configuration_manager = ConfigurationManager(parsed_list=parsed_list)
    configuration = configuration_manager.generate_configuration()
    for project in configuration.projects:
        provider.create_or_update_project(project)


if __name__ == "__main__":
    main()
