import json


class ProjectManFileNotFoundError(Exception):
    pass


class ProjectManInvalidJsonFileError(Exception):
    pass


class Base:
    @property
    def class_name(self):
        return self.__class__.__name__


class Configuration:
    def __init__(self):
        pass


class JsonParser(Base):
    def parse(self, filepath=".projectman.json"):
        try:
            f = open(filepath)
        except FileNotFoundError:
            raise ProjectManFileNotFoundError(
                f"{self.class_name}:: error: file {filepath} not found"
            )

        try:
            json_file = json.load(f)
        except json.decoder.JSONDecodeError:
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {filepath} is invalid"
            )
        return Configuration()


def main():
    parser = JsonParser()
    configuration = parser.parse()


if __name__ == "__main__":
    main()
