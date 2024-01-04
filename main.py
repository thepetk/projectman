from configuration import ConfigurationManager
from parsers import JsonParser
from providers import GithubProvider
from utils import PROJECTMAN_FILEPATH, REPO_NAME, logger, now


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
    logger.info(
        "%s::INFO::main::getting configuration file %s from repo %s"
        % (now(), PROJECTMAN_FILEPATH, REPO_NAME)
    )
    config_file = provider.get_configuration_file(PROJECTMAN_FILEPATH)
    parsed_list = parser.parse(config_file)
    # Upsert all given projects
    configuration = configuration_manager.generate_configuration(parsed_list)
    logger.info(
        "%s::INFO::main::found %s projects" % (now(), len(configuration.projects))
    )
    for project in configuration.projects:
        logger.info(
            "%s::INFO::main::applying changes for project %s" % (now(), project.name)
        )
        provider.create_or_update_project(project)


if __name__ == "__main__":
    main()
