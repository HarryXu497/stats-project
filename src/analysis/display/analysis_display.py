

from collections.abc import Callable, Mapping, Sequence
import os
from pathlib import Path
from display.plots.display import Display
from input.config_reader import ConfigData
from input.data_reader import Data, MonthlyHousingData


class AnalysisDisplay:
    __slots__ = '_data', '_config', '_display_registry'

    def __init__(self, *, data: Data, config: ConfigData, display_registry: Mapping[str, Callable[..., Display]]):
        self._data = data
        self._config = config
        self._display_registry = display_registry
    
    def output(self, *, show_display=False):
        for display_key, output_directory in self._config.output.items():
            display_callable = self._display_registry[display_key]
            display = display_callable(self._data)

            # Generate appropriate filepath

            current_filepath = os.path.abspath(os.curdir)
            full_directory_path = os.path.join(current_filepath, output_directory)

            Path(full_directory_path).mkdir(parents=True, exist_ok=True)

            display.output(
                output_path=full_directory_path,
                show_display=show_display,
            )



        # ParallelBoxplot(self._data).output()
        # Histogram(self._data).output()
        