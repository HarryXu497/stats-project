from collections.abc import Sequence

import matplotlib as plt
from matplotlib.figure import Figure
import pandas as pd
from input.data_reader import _MonthlyData
import seaborn as sns

_index_to_short_month = {
    0: "jan",
    1: "feb",
    2: "mar",
    3: "apr",
    4: "may",
    5: "jun",
    6: "jul",
    7: "aug",
    8: "sep",
    9: "oct",
    10: "nov",
    11: "dec",
}

_housing_type_map = {
    "composite_hpi": "cmp",
    "single_family_detached_hpi": "sfd",
    "single_family_attached_hpi": "sfa",
    "townhouse_hpi": "twn",
    "apartment_hpi": "apt",
}

class Histogram:
    def __init__(self, data: Sequence[_MonthlyData]):
        self._data = data
        self._processed_data = self._process()
    
    def _process(self):
        processed_data =  [(column, self._process_column(column)) for column in _MonthlyData.col_names[1:]]

        housing_type_augmented_data = (df.assign(htype=_housing_type_map[col_name]) for col_name, df in processed_data)
        concatenated_data = pd.concat([data for data in housing_type_augmented_data])

        return concatenated_data

    def _process_column(self, col_name: str):
        entries: list[tuple[int, float]] = []

        for monthly_data in self._data:
            df = monthly_data.data

            series = df[col_name].dropna()
            series = series[series != "-"]
            series = series.astype(float)
            series = series[series != 0]


            for value in series.array:
                entries.append((monthly_data.year, value))

        entries.sort()

        return pd.DataFrame(
            data={
                # For 2 year periods
                # "year": [f"{entry[0] - 1}-{entry[0]}" if entry[0] % 2 == 1 else f"{entry[0]}-{entry[0] + 1}" for entry in entries],
                "year": [entry[0] for entry in entries],
                "hpi": [entry[1] for entry in entries],
            }
        )
        
    def show(self):
        sns.set_theme()
        g = sns.FacetGrid(self._processed_data, row="htype", col="year", margin_titles=True)
        g.map(sns.histplot, "hpi")
        g.tight_layout()
        # g.figure.subplots_adjust(left=None, bottom=None,  right=None, top=None, wspace=None, hspace=None)

        # TODO: TEMP 
        plt.pyplot.savefig("test.png")
        # plt.pyplot.show() 
