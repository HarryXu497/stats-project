from dataclasses import dataclass
import json
import typing


class ProcessConfigReader:
    def __init__(self, source: typing.TextIO):
        config_dict = json.load(source)

        self._config_dict = _ProcessConfig(
            sources=tuple(config_dict["sources"]),
            output=str(config_dict["output"]),
        )

        # TODO: validate

    @property
    def config(self):
        return self._config_dict

@dataclass(frozen=True, slots=True, kw_only=True)
class _ProcessConfig:
    sources: tuple[str]
    output: str