from collections import deque
from collections.abc import Mapping
import os
from pathlib import Path

from input.config_reader import ConfigData
from processor.processors import Processor


class DataProcessor:
    __slots__ = '_config', '_processors'

    def __init__(self, *, config: ConfigData, processors: Mapping[str, Processor]):
        self._config = config
        self._processors = processors

    def process_all(self):
        # Exhaust the generator in the fastest way possible
        deque(self._process_generator(), maxlen=0)
    
    def _process_generator(self):
        for source in self._config.sources:
            input_directory = source.directory
            output_directory = source.output
            processor_key = source.processor
            for dirpath, _, filenames in os.walk(input_directory):
                for filename in filenames:
                    # Generate appropriate filepaths
                    current_filepath = os.path.abspath(os.curdir)
                    full_filepath = os.path.join(current_filepath, dirpath, filename)
                    relative_filepath = os.path.relpath(full_filepath, input_directory)
                    output_filepath = os.path.join(current_filepath, output_directory, relative_filepath)
                    output_dirpath = os.path.normpath(os.path.join(output_filepath, ".."))


                    try:
                        Path(output_dirpath).mkdir(parents=True, exist_ok=True)

                        processor = self._processors[processor_key]

                        with open(full_filepath, "r") as f:
                            # Dispatch processor
                            output = processor.process(f)

                        with open(output_filepath, "w+") as f:
                            f.write(output)
                    except ValueError:
                        print(f"Invalid data for file {full_filepath}.")
                    except IOError as e:
                        print("An IO error occurred.")
                        print(e)
                    
                    yield

