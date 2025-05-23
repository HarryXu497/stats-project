
from transform.transformer import HPITransformer, ListingsTransformer
from display.plots.scatterplot import Scatterplot
from display.plots.histogram import Histogram
from display.plots.parallel_boxplot import ParallelBoxplot
from display.analysis_display import AnalysisDisplay
from input.data_reader import DataReader
from input.config_reader import ConfigReader


def main():
    with open("analysis_config.json") as config_file:
        reader = ConfigReader(config_file)

    data_reader = DataReader(
        config=reader.config,
        transformer_registry={
            "HPITransformer": HPITransformer,
            "ListingsTransformer": ListingsTransformer,
        }
    )

    display = AnalysisDisplay(
        data=data_reader.read_all(),
        config=reader.config,
        display_registry={
            "ParallelBoxplot": ParallelBoxplot,
            "Histogram": Histogram,
            "Scatterplot": Scatterplot
        }
    )

    display.output()

if __name__ == "__main__":
    main()