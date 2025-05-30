from pathlib import Path
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt
from display.plots.scatterplot import Scatterplot
from display.plots.display import Display
from input.data_reader import Data

class ResidualsPlot(Display):
    def __init__(self, data: Data):
        self._data = data
        self._processed_data = Scatterplot(data)._process()
    
    def output(self, *, output_path: Path | str, show_display=False):
        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        sns.set_theme()
        g = sns.FacetGrid(self._processed_data, row="month")
        g.map_dataframe(sns.residplot, x="counts", y="hpi")

        g.tight_layout()

        title = f"Residuals Plot of Airbnb Listing Counts vs. HPI by Month, with Outliers"
        filepath = output_path / f"{title}.png"
        g.figure.subplots_adjust(top=0.90)
        g.figure.suptitle(title, fontsize=36, wrap=True)
        g.figure.set_size_inches(5, 36)

        plt.savefig(filepath)

        if show_display:
            plt.show() 
        else:
            plt.close()
