from typing import Any

from orjson import orjson


class FormParserMixin:
    @classmethod
    def validate(cls: "Type['Model']", value: Any) -> 'Model':
        if isinstance(value, str):
            value = orjson.loads(value)
        return super().validate(value)
