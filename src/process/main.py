
from processor.data_processor import DataProcessor
from process.input.config_reader import ConfigReader
from processor.processors import SpaceSeparatedTextNoLabelProcessor


def main():
    with open("process_config.json") as config_file:
        reader = ConfigReader(config_file)

    processor = DataProcessor(
        config=reader.config,
        processor=SpaceSeparatedTextNoLabelProcessor()
    )
    processor.process_all()

if __name__ == "__main__":
    main()