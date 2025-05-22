from collections import deque
import os
from pathlib import Path

from process.input.config_reader import ConfigData
from process.processor.processors import Processor


class DataProcessor:
    __slots__ = '_config', '_processor'

    def __init__(self, *, config: ConfigData, processor: Processor):
        self._config = config
        self._processor = processor

    def process_all(self):
        # Exhaust the generator in the fastest way possible
        deque(self._process_generator(), maxlen=0)
    
    def _process_generator(self):
        for source in self._config.sources:
            for dirpath, _, filenames in os.walk(source):
                for filename in filenames:
                    # Generate appropriate filepaths
                    current_filepath = os.path.abspath(os.curdir)
                    full_filepath = os.path.join(current_filepath, dirpath, filename)
                    relative_filepath = os.path.relpath(full_filepath, source)
                    output_filepath = os.path.join(current_filepath, self._config.output, relative_filepath)
                    output_dirpath = os.path.normpath(os.path.join(output_filepath, ".."))

                    with open(full_filepath, "r") as f:
                        content = f.read()

                    try:
                        Path(output_dirpath).mkdir(parents=True, exist_ok=True)

                        # Dispatch processor
                        output = self._processor.process(content)

                        with open(output_filepath, "w+") as f:
                            f.write(output)
                    except ValueError:
                        print(f"Invalid data for file {full_filepath}.")
                    except IOError as e:
                        print("An IO error occurred.")
                        print(e)
                    
                    yield

