import math
from pathlib import Path
import pandas as pd 
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt
from collections.abc import Sequence
from display.plots.display import Display
from input.data_reader import Data, MonthlyHousingData

_index_to_short_month = {
    0: "jan",
    1: "feb",
    2: "mar",
    3: "apr",
    4: "may",
    5: "jun",
    6: "jul",
    7: "aug",
    8: "sep",
    9: "oct",
    10: "nov",
    11: "dec",
}


class Scatterplot(Display):
    def __init__(self, data: Data):
        self._data = data
        self._processed_data = self._process()
    
    def _process(self):
        data = self._process_column("composite_hpi")


        listing_data = self._process_listings()

        joined_data = (data.merge(listing_data, left_on=['area', 'numeric_month', 'year'], right_on=['district', 'numeric_month', 'year'])
          .reindex())
        
        joined_data = joined_data.sort_values(by=["year", "numeric_month"])
        joined_data = joined_data.assign(month=joined_data["numeric_month"].apply(lambda x: _index_to_short_month[x]) + " " + joined_data['year'].astype(str))

        joined_data["counts"] = joined_data["counts"].apply(lambda x: math.sqrt(x))

        return joined_data

    def _process_listings(self):
        monthly_listing_data = self._data.listing_counts_data

        entries: Sequence[pd.DataFrame] = []

        for listing_data in monthly_listing_data:
            df = listing_data.data

            df = df.assign(numeric_month=listing_data.month, year=listing_data.year)

            entries.append(df)
        
        df = pd.concat(entries)

        return df

    def _process_column(self, col_name: str):
        entries: Sequence[pd.DataFrame] = []

        for monthly_data in self._data.monthly_housing_data:
            df = monthly_data.data
            
            df = df[["area", col_name]].dropna()

            # Extract the District Code from the string "Toronto <CODE>"
            df["area"] = df["area"].str.slice(8)
            df = df[df[col_name] != "-"]
            df = df.astype({
                col_name: float,
            })
            df = df[df[col_name] != 0]

            df = df.assign(numeric_month=monthly_data.month, year=monthly_data.year)
            df = df.rename(columns={ col_name: "hpi" })


            entries.append(df)

        df = pd.concat(entries)
        df = df.sort_values(by=['year', 'numeric_month'])

        df = df.groupby(['area', 'numeric_month', 'year']).median(numeric_only=True)
        df = df.reset_index()

        return df
    
    def output(self, *, output_path: Path | str, show_display=False):
        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        sns.set_theme()
        g = sns.lmplot(self._processed_data, x="counts", y="hpi", row="month")

        def annotate(data, **_):
            r, p = sp.stats.pearsonr(data['counts'], data['hpi'])
            ax = plt.gca()
            ax.text(0.05, .90, 'r={:.2f}, R^2={:.2g}, p={:.2g}'.format(r, r * r, p),
                    transform=ax.transAxes)
            
        g.map_dataframe(annotate)

        g.tight_layout()

        title = f"Relational Plot of sqrt(Airbnb Listing Counts) vs. Composite HPI by Month"
        
        filepath = output_path / f"{title}.pdf"
        g.figure.subplots_adjust(top=0.90)
        g.figure.suptitle(title, fontsize=36, wrap=True)
        g.figure.set_size_inches(5, 36)

        plt.savefig(filepath)

        if show_display:
            plt.show() 
        else:
            plt.close()
