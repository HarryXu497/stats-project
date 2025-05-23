from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import os
from pathlib import Path
import pandas as pd

from transform.transformer import ListingCountsData, MonthlyHousingData, Transformer
from input.config_reader import ConfigData

class DataReader:
    __slots__ = '_config', '_tranformer_registry'

    def __init__(self, config: ConfigData, transformer_registry: Mapping[str, Transformer]):
        self._config = config
        self._tranformer_registry = transformer_registry
    
    def read_all(self):
        monthly_housing_data = []
        listing_counts_data = []

        for item in self._generator():
            if isinstance(item, MonthlyHousingData):
                monthly_housing_data.append(item)
            elif isinstance(item, ListingCountsData):
                listing_counts_data.append(item)
        
        return Data(
            monthly_housing_data=monthly_housing_data,
            listing_counts_data=listing_counts_data,
        )
    
    def _generator(self):
        for source, source_data in self._config.sources.items():
            for dirpath, _, filenames in os.walk(source):
                for filename in filenames:
                    # Generate appropriate filepaths
                    current_filepath = os.path.abspath(os.curdir)
                    full_filepath = os.path.join(current_filepath, dirpath, filename)

                    # Dispatch transformer
                    transformer = self._tranformer_registry[source_data.transformer]

                    path = Path(full_filepath)

                    yield transformer().transform(path)


@dataclass(frozen=True, slots=True, kw_only=True)
class Data:
    monthly_housing_data: Sequence[MonthlyHousingData]
    listing_counts_data: Sequence[ListingCountsData]