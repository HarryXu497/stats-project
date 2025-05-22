

from display.plots.parallel_boxplot import ParallelBoxplot
from input.data_reader import _MonthlyData


class AnalysisDisplay:
    __slots__ = '_data'
    
    def __init__(self, data: list[_MonthlyData]):
        self._data = data
    
    def show(self):
        # TODO: temp
        ParallelBoxplot(self._data).show()