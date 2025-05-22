import os
from pathlib import Path

from input.process_config_reader import _ProcessConfig
from processor.processor import Processor


class DataProcessor:
    def __init__(self, *, config: _ProcessConfig, processor: Processor):
        self._config = config
        self._processor = processor

    
    def process_all(self):
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

                        output = self._processor.process(content)

                        with open(output_filepath, "w+") as f:
                            f.write(output)
                    except ValueError:
                        print(f"Invalid data for file {full_filepath}.")
                    except IOError as e:
                        print("An IO error occurred.")
                        print(e)

