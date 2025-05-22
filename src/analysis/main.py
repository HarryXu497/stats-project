
from display.display import AnalysisDisplay
from input.data_reader import DataReader
from input.config_reader import ConfigReader


def main():
    with open("analysis_config.json") as config_file:
        reader = ConfigReader(config_file)

    data_reader = DataReader(
        config=reader.config,
    )

    display = AnalysisDisplay(data_reader.read_all())

    display.show()

if __name__ == "__main__":
    main()