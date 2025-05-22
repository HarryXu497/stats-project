from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
import typing


class ConfigReader:
    __slots__ = '_config_dict'

    def __init__(self, source: typing.TextIO):
        config_dict = json.load(source)

        self._config_dict = ConfigData(
            sources=[
                SourceData(
                    directory=directory,
                    processor=source_data["processor"],
                    output=source_data["output"],
                ) 
                for directory, source_data in config_dict["sources"].items()
            ],
        )

        # TODO: validate

    @property
    def config(self):
        return self._config_dict
    
@dataclass(frozen=True, slots=True, kw_only=True)
class SourceData:
    directory: str
    processor: str
    output: str

@dataclass(frozen=True, slots=True, kw_only=True)
class ConfigData:
    sources: Sequence[SourceData]
