from collections.abc import Sequence
from pathlib import Path
import matplotlib as plt
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
from input.data_reader import Data, MonthlyHousingData

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


class ParallelBoxplot:
    __slots__ = '_data', '_processed_data'

    def __init__(self, data: Data):
        self._data = data
        self._processed_data = self._process()
    
    def _process(self):
        return [(column, self._process_column(column)) for column in MonthlyHousingData.col_names[1:]]

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
            df = df.assign(year=monthly_data.year, short_month=monthly_data.month)

            entries.append(df)

        df = pd.concat(entries)
        df = df.sort_values(by=["year", "short_month"])
        df["short_month"] = df["short_month"].apply(lambda x: _index_to_short_month[x])
        df = df.assign(month=df['short_month'] + " " + df['year'].astype(str))


        return df
    
    def output(self, *, output_path: Path | str, show_display=False):
        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        sns.set_theme()
        for column, data in self._processed_data:
            title = f"Parallel Boxplots of {column} vs. Month"

            filepath = output_path / f"{title}.png"

            fig: Figure = plt.pyplot.figure()
            axes = sns.boxplot(data=data, x="month", y="hpi")
            axes.tick_params(axis='x', rotation=90, labelsize=8)
            axes.set_title(title)
            fig.set_size_inches(26, 14)
            # fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

            plt.pyplot.savefig(filepath)

            if not show_display:
                plt.pyplot.close()

        if show_display:
            plt.pyplot.show() 
