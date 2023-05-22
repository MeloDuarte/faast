"""Module Assignment 1: EU Life Expectancy"""

import argparse
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from life_expectancy.read_and_write import load_data, save_data

def clean_data(expectancy_wide: DataFrame, country: str = 'PT') -> DataFrame:
    """
    Unpivots the DataFrame to long format, ensures `year` is an `int` 
    (with the appropriate data cleaning if required), ensures `value` 
    is a `float` (with the appropriate data cleaning if required, 
    and do remove the NaNs) and filters the data by region.
    :param expectancy_wide: expectancy DataFrame in wide format.
    :param country: region where to filter data.
    :return: cleaned DataFrame
    """

    expectancy_lg = pd.melt(expectancy_wide, id_vars=expectancy_wide.columns[0], var_name="year")

    expectancy_lg[['unit', 'sex', 'age', 'region']] = pd.DataFrame(
        expectancy_lg[expectancy_lg.columns[0]].str.split(',', expand=True),
        index=expectancy_lg.index
    )

    expectancy_region = expectancy_lg[expectancy_lg['region'].str.upper() == country.upper()]

    expectancy_clean = expectancy_region[expectancy_region['year'].str.strip().str.isdigit()]

    # Find all occurrences of floats in column `value`
    # and converts argument to numeric type. Returns NaN otherwise.
    value_floats = expectancy_clean['value'].str.findall(r"\-?\d+\.\d+")
    expectancy_clean['value'] = pd.to_numeric(value_floats[value_floats.str.len() == 1].str[0])

    # Drops all NaN rows in columns `year` and `value`
    expectancy_clean = expectancy_clean.dropna(subset=['year', 'value'])

    expectancy_clean['year'] = expectancy_clean['year'].astype(int)

    expectancy_result = expectancy_clean[['unit', 'sex', 'age', 'region', 'year', 'value']]

    return expectancy_result


def main(country: str='PT') -> None:
    """Loads, cleans and saves data.
    :param country: region where to filter data. 
    """
    filename = Path(__file__).parent / "data/eu_life_expectancy_raw.tsv"
    expectancy = load_data(filename)
    expectancy_cleaned = clean_data(expectancy, country)
    save_data(expectancy_cleaned)

    return expectancy_cleaned


if __name__ == "__main__":  # pragma: no cover
    # Country command-line option. (the default should be `PT`)
    parser = argparse.ArgumentParser()
    parser.add_argument("-country", default="PT", help="Filters data by `country`")
    args = parser.parse_args()

    main(args.country)
