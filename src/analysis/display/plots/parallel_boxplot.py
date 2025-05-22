import matplotlib as plt
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
from input.data_reader import _MonthlyData

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

    def __init__(self, data: list[_MonthlyData]):
        self._data = data
        self._processed_data = self._process()
    
    def _process(self):
        return [(column, self._process_column(column)) for column in _MonthlyData.col_names[1:]]

    def _process_column(self, col_name: str):
        entries: list[tuple[int, int, float]] = []

        for monthly_data in self._data:
            df = monthly_data.data

            series = df[col_name].dropna()
            series = series[series != "-"]
            series = series.astype(float)
            series = series[series != 0]


            for value in series.array:
                entries.append((monthly_data.year, monthly_data.month, value))

        entries.sort()

        return pd.DataFrame(
            data={
                "month": [f"{_index_to_short_month[entry[1]]} {entry[0]}" for entry in entries],
                "hpi": [entry[2] for entry in entries],
            }
        )

    
    def show(self):
        # print(self._processed_data)
        sns.set_theme()
        for column, data in self._processed_data:
            fig: Figure = plt.pyplot.figure()
            axes = sns.boxplot(data=data, x="month", y="hpi")
            axes.tick_params(axis='x', rotation=90, labelsize=8)
            axes.set_title(f"Parallel Boxplots of {column} vs. Month")

            fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

        plt.pyplot.show() 