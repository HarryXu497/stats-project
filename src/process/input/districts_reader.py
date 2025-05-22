from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
import typing


class DistrictsReader:
    __slots__ = '_district_dict'

    def __init__(self, source: typing.TextIO):
        district_to_neighborhoods_dict: Mapping[str, Sequence[str]] = json.load(source)

        # TODO: validate

        self._district_dict: Mapping[str, str] = {}

        for district, neighborhoods in district_to_neighborhoods_dict.items():
            for neighborbood in neighborhoods:
                self._district_dict[neighborbood] = district


    @property
    def districts_mapping(self):
        return self._district_dict
