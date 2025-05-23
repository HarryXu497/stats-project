from pathlib import Path
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from collections.abc import Sequence
from display.plots.display import Display
from input.data_reader import Data, MonthlyHousingData

_housing_type_map = {
    "composite_hpi": "cmp",
    "single_family_detached_hpi": "sfd",
    "single_family_attached_hpi": "sfa",
    "townhouse_hpi": "twn",
    "apartment_hpi": "apt",
}


class Scatterplot(Display):
    def __init__(self, data: Data):
        self._data = data
        self._processed_data = self._process()

        print(self._processed_data)
    
    def _process(self):
        processed_data =  [self._process_column(column) for column in MonthlyHousingData.col_names[1:]]
        concatenated_data = pd.concat(processed_data)

        listing_data = self._data.listing_counts_data[0].data

        joined_data = (concatenated_data.merge(listing_data, left_on='area', right_on='district')
          .reindex())

        return joined_data

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

            df = df.assign(year=monthly_data.year, htype=_housing_type_map[col_name])
            df = df.rename(columns={ col_name: "hpi" })

            entries.append(df)

        df = pd.concat(entries)
        df = df.sort_values(by=['year'])

        return df
    
    def output(self, *, output_path: Path | str, show_display=False):
        if not isinstance(output_path, Path):
            output_path = Path(output_path)

        sns.set_theme()
        g = sns.relplot(self._processed_data, x="hpi", y="counts", row="year", hue="htype")
        g.tight_layout()

        title = f"Relational Plot of HPI vs. Airbnb Listing Counts by Year and Housing Type"
        filepath = output_path / f"{title}.png"
        g.figure.suptitle(title)

        plt.savefig(filepath)

        if show_display:
            plt.show() 
        else:
            plt.close()
