
from input.districts_reader import DistrictsReader
from processor.data_processor import DataProcessor
from input.config_reader import ConfigReader
from processor.processors import HPIProcessor, ListingsProcessor


def main():
    with open("process_config.json") as config_file:
        config_reader = ConfigReader(config_file)

    with open("districts.json") as district_file:
        districts_reader = DistrictsReader(district_file)

    processor = DataProcessor(
        config=config_reader.config,
        processors={
            "HPIProcessor": HPIProcessor(),
            "ListingsProcessor": ListingsProcessor(districts_reader.districts_mapping),
        }
    )
    processor.process_all()

if __name__ == "__main__":
    main()