from dataclasses import dataclass
import json
import typing


class ConfigReader:
    __slots__ = '_config_dict'
    
    def __init__(self, source: typing.TextIO):
        config_dict = json.load(source)

        self._config_dict = ConfigData(
            sources=tuple(config_dict["sources"]),
        )

        # TODO: validate

    @property
    def config(self):
        return self._config_dict

@dataclass(frozen=True, slots=True, kw_only=True)
class ConfigData:
    sources: tuple[str]