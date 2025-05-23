from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import typing

import pandas as pd


_month_to_index = {
    "january": 0,
    "february": 1,
    "march": 2,
    "april": 3,
    "may": 4,
    "june": 5,
    "july": 6,
    "august": 7,
    "september": 8,
    "october": 9,
    "november": 10,
    "december": 11,
}


class Transformer(ABC):
    @abstractmethod
    def transform(self, filepath: Path) -> typing.Any:
        pass

class HPITransformer(Transformer):
    def transform(self, filepath: Path):
        year = int(filepath.parts[-2])
        month = _month_to_index[filepath.stem]

        data = pd.read_csv(filepath)
            
        return MonthlyHousingData(
            year=year,
            month=month,
            data=data
        )

class ListingsTransformer(Transformer):
    def transform(self, filepath: Path):
        data = pd.read_csv(filepath)
            
        return ListingCountsData(
            data=data
        )

@dataclass(frozen=True, slots=True, kw_only=True)
class MonthlyHousingData:
    year: int
    month: int
    data: pd.DataFrame

    labels: typing.ClassVar = [
        "Toronto W01",
        "Toronto W02",
        "Toronto W03",
        "Toronto W04",
        "Toronto W05",
        "Toronto W06",
        "Toronto W07",
        "Toronto W08",
        "Toronto W09",
        "Toronto W10",
        "Toronto C01",
        "Toronto C02",
        "Toronto C03",
        "Toronto C04",
        "Toronto C06",
        "Toronto C07",
        "Toronto C08",
        "Toronto C09",
        "Toronto C10",
        "Toronto C11",
        "Toronto C12",
        "Toronto C13",
        "Toronto C14",
        "Toronto C15",
        "Toronto E01",
        "Toronto E02",
        "Toronto E03",
        "Toronto E04",
        "Toronto E05",
        "Toronto E06",
        "Toronto E07",
        "Toronto E08",
        "Toronto E09",
        "Toronto E10",
        "Toronto E11",
    ]
    col_names: typing.ClassVar = [
        "area",
        "composite_hpi",
        "single_family_detached_hpi",
        "single_family_attached_hpi",
        "townhouse_hpi",
        "apartment_hpi",
    ]

    def __post_init__(self):
        if self.month < 0 or self.month > 11:
            raise ValueError("Parameter 'month' must be between 0 and 11 inclusive.")
        
        if self.year < 0:
            raise ValueError("Parameter 'year' must be positive.")

@dataclass(frozen=True, slots=True, kw_only=True)
class ListingCountsData:
    data: pd.DataFrame
