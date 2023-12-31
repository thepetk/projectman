from configuration import ConfigurationManager
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
    configuration_manager = ConfigurationManager()

    # Transform projectman file into config object.
    config_file = provider.get_configuration_file(PROJECTMAN_FILEPATH)
    parsed_list = parser.parse(config_file)
    # Upsert all given projects
    configuration = configuration_manager.generate_configuration(parsed_list)
    for project in configuration.projects:
        provider.create_or_update_project(project)


if __name__ == "__main__":
    main()
