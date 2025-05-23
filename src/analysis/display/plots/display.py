

from abc import ABC, abstractmethod
from pathlib import Path

class Display(ABC):
    @abstractmethod
    def output(self, *, output_path: Path | str, show_display=False):
        pass
