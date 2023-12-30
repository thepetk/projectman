from typing import Any, Optional

from exceptions import ProjectManValidationError
from utils import CONFIGURATION_VALUE, Base


class FieldValidator(Base):
    def __init__(
        self,
        is_one_of: Optional[list[str]] = None,
        is_instance: Any = None,
        default: Optional[str] = None,
        optional: bool = True,
    ) -> None:
        self.is_one_of = is_one_of
        self.is_instance = is_instance
        self.default = default
        self.optional = optional

    def validate(self, key: str, value: CONFIGURATION_VALUE) -> CONFIGURATION_VALUE:
        if self.is_one_of is not None:
            return value if value in self.is_one_of else self.default
        elif self.is_instance is not None:
            if isinstance(value, self.is_instance):
                return value
            elif value is None and self.default is not None:
                return self.default
            elif value is None and self.optional is True:
                return value
            else:
                raise ProjectManValidationError(
                    f"error: invalid type. Key {key} of type {self.is_instance} has type {type(value)}"  # noqa: E501
                )
        else:
            return value
