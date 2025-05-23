from collections.abc import Sequence, Mapping
from dataclasses import dataclass
import json
import typing


class ConfigReader:
    __slots__ = '_config_dict'
    
    def __init__(self, source: typing.TextIO):
        config_dict = json.load(source)

        self._config_dict = ConfigData(
            sources={
                source: SourceData(
                    transformer=source_data["transformer"]
                )
                for source, source_data in config_dict["sources"].items()
            },
            output=config_dict["output"]
        )

        print(self._config_dict)

        # TODO: validate

    @property
    def config(self):
        return self._config_dict


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceData:
    transformer: str

@dataclass(frozen=True, slots=True, kw_only=True)
class ConfigData:
    sources: Mapping[str, SourceData]
    output: Mapping[str, str]