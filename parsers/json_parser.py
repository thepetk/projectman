import json

from configuration import ConfigurationFile
from exceptions import (
    FieldNotInConfigurationFieldsError,
    FieldValidatorNotExistsError,
    ProjectManInvalidJsonFileError,
)
from utils import (
    ALL,
    CONFIGURATION_DICT,
    CONFIGURATION_ITEM_ACCEPTED_TYPES,
    CONFIGURATION_VALUE,
    Base,
)
from validators import FieldValidator

# Optional and Required fields inside .projectman.json
CONFIGURATION_FIELDS = {
    "name": FieldValidator(is_instance=str, default="ProjectMan Project"),
    "description": FieldValidator(is_instance=str, default=""),
    "labels": FieldValidator(is_instance=list, default=[]),
    "assignees": FieldValidator(is_instance=list, default=[]),
    "reviewers": FieldValidator(is_instance=list, default=[]),
    "milestones": FieldValidator(is_instance=list, default=[]),
    "created_on": FieldValidator(is_instance=str, default=""),
    "last_updated_on": FieldValidator(is_instance=str, default=""),
    "closed_on": FieldValidator(is_instance=str, default=""),
    "type": FieldValidator(is_one_of=CONFIGURATION_ITEM_ACCEPTED_TYPES, default=ALL),
}


class JsonParser(Base):
    def _getkey(
        self,
        json_dict: CONFIGURATION_DICT,
        key: CONFIGURATION_VALUE,
    ) -> CONFIGURATION_VALUE:
        if key not in CONFIGURATION_FIELDS.keys():
            raise FieldNotInConfigurationFieldsError(
                f"error: invalid field. Field {key} is not a valid configuration field"
            )
        if not isinstance(CONFIGURATION_FIELDS.get(key), FieldValidator):
            raise FieldValidatorNotExistsError(
                f"error: no field validator defined for key {key}"
            )
        return CONFIGURATION_FIELDS[key].validate(key, json_dict.get(key))

    def parse(self, config_file: ConfigurationFile) -> list[CONFIGURATION_DICT]:
        parsed_list = []
        try:
            json_dict_list = json.loads(config_file.content)
        except json.decoder.JSONDecodeError:
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {config_file.filepath} is invalid"
            )

        if not isinstance(json_dict_list, list):
            raise ProjectManInvalidJsonFileError(
                f"{self.class_name}:: error: file {config_file.filepath} is not a list"
            )
        for json_dict in json_dict_list:
            parsed_list.append(
                {
                    key: self._getkey(json_dict, key)
                    for key in CONFIGURATION_FIELDS.keys()
                }
            )
        return parsed_list
