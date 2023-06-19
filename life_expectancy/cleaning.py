"""Module Assignment 1: EU Life Expectancy"""

import argparse
from pathlib import Path
import pandas as pd
from life_expectancy.strategies import (
    save_data,
    LoadDataStrategy,
    LoadTSVDataStrategy,
    LoadJSONDataStrategy,
    Region
)

class MainCleaning: # pylint: disable=too-few-public-methods
    """
    A class that performs cleaning operations on
    life expectancy dataset using a specified strategy.

    :param filename: The name of the file containing the life expectancy dataset.
    :param strategy: An instance of a cleaning strategy object.
    :param country: The name of the country for which the data needs to be filtered.
    """
    def __init__(self, filename: str, strategy: LoadDataStrategy, country: Region=Region.PT):
        self.filename = filename
        self.strategy = strategy
        self.country = country

    def do_cleaning(self) -> pd.DataFrame:
        """
        Performs the cleaning operation on the life expectancy dataset.
        :return: The cleaned life expectancy dataset.
        """
        expectancy = self.strategy.load_data(self.filename)
        expectancy_cleaned = self.strategy.clean_data(expectancy, self.country)
        return expectancy_cleaned


def main(country: Region=Region.PT, loader: str='tsv') -> None:
    """Loads, cleans and saves data.
    :param country: region where to filter data. 
    :param loader: load file type. 
    """
    cleaning = None
    if loader == 'tsv':
        filename = Path(__file__).parent / "data/eu_life_expectancy_raw.tsv"
        cleaning = MainCleaning(filename, LoadTSVDataStrategy(), country)
    else:
        filename = Path(__file__).parent / "data/eurostat_life_expect.json"
        cleaning = MainCleaning(filename, LoadJSONDataStrategy(), country)

    expectancy_cleaned = cleaning.do_cleaning()
    save_data(expectancy_cleaned)

    return expectancy_cleaned


if __name__ == "__main__":  # pragma: no cover
    # Country command-line option. (the default should be `PT`)
    # Format command-line option. (the default should be `tsv`)
    parser = argparse.ArgumentParser()
    parser.add_argument("-country", default=Region.PT, help="Filters data by `country`")
    parser.add_argument("-format", default="tsv", help="Load file type")
    args = parser.parse_args()

    main(args.country, args.format)
