from dataclasses import dataclass
import json
import typing


class AnalysisConfigReader:
    def __init__(self, source: typing.TextIO):
        config_dict = json.load(source)

        self._config_dict = _AnalysisConfig(
            sources=tuple(config_dict["sources"]),
        )

        # TODO: validate

    @property
    def config(self):
        return self._config_dict

@dataclass(frozen=True, slots=True, kw_only=True)
class _AnalysisConfig:
    sources: tuple[str]