from collections.abc import Sequence
from pathlib import Path

import matplotlib as plt
import pandas as pd
from display.plots.display import Display
from input.data_reader import Data, MonthlyHousingData
import seaborn as sns


_housing_type_map = {
    "composite_hpi": "cmp",
    "single_family_detached_hpi": "sfd",
    "single_family_attached_hpi": "sfa",
    "townhouse_hpi": "twn",
    "apartment_hpi": "apt",
}

class Histogram(Display):
    def __init__(self, data: Data):
        self._data = data
        self._processed_data = self._process()
    
    def _process(self):
        processed_data =  [self._process_column(column) for column in MonthlyHousingData.col_names[1:]]
        concatenated_data = pd.concat(processed_data).reindex()

        return concatenated_data

    def _process_column(self, col_name: str):
        entries: Sequence[pd.DataFrame] = []

        for monthly_data in self._data.monthly_housing_data:
            df = monthly_data.data
            
            series: pd.Series = df[col_name].dropna()

            # Extract the District Code from the string "Toronto <CODE>"
            series = series[series != "-"]
            series = series.astype(float)
            series = series[series != 0]

            series = series.rename("hpi")
            df = series.to_frame()
            df = df.assign(year=monthly_data.year, htype=_housing_type_map[col_name])

            entries.append(df)

        df = pd.concat(entries)
        df = df.sort_values(by=["year"])

        return df
        
    def output(self, *, output_path: Path | str, show_display=False):
        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        sns.set_theme()
        g = sns.FacetGrid(self._processed_data, row="year", col="htype", margin_titles=True)
        g.map(sns.histplot, "hpi")
        g.tight_layout()

        title = f"Distribution of HPI by Year and Housing Type"
        filepath = output_path / f"{title}.png"
        g.figure.subplots_adjust(top=0.95)
        g.figure.suptitle(title, fontsize=48)

        plt.pyplot.savefig(filepath)

        if show_display:
            plt.pyplot.show() 
        else:
            plt.pyplot.close()
