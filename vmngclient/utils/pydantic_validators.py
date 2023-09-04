from pydantic import BaseModel, root_validator


class ConvertBoolToStringModel(BaseModel):
    @root_validator  # type: ignore
    def convert_bool_to_string_validator(cls, values):
        for key, value in values.items():
            if isinstance(value, bool):
                values[key] = str(value).lower()
        return values
