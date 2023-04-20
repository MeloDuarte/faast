"""Module Assignment 1: EU Life Expectancy"""

import argparse
import pandas as pd
from pandas import DataFrame


def load_data() -> DataFrame:
    """
    Loads `eu_life_expectancy_raw.tsv` DataFrame.
    :return: DataFrame loaded.
    """
    data = pd.read_csv(
        "life_expectancy/data/eu_life_expectancy_raw.tsv",
        sep='\t',
        header=0
    )

    return data


def save_data(expectancy_result: DataFrame) -> None:
    """
    Save the resulting DataFrame to `pt_life_expectancy.csv`.
    :param expectancy_result: DataFrame cleaned to be saved.
    """
    expectancy_result.to_csv(
        'life_expectancy/data/pt_life_expectancy.csv',
        index=False
    )


def clean_data(expectancy_wide: DataFrame, country: str) -> DataFrame:
    """
    Unpivots the DataFrame to long format, and cleans data.
    :param expectancy_wide: expectancy DataFrame in wide format.
    :param country: region where to filter data.
    :return: cleaned DataFrame
    """

    expectancy_lg = pd.melt(expectancy_wide, id_vars=expectancy_wide.columns[0], var_name="year")

    expectancy_lg[['unit', 'sex', 'age', 'region']] = pd.DataFrame(
        expectancy_lg[expectancy_lg.columns[0]].str.split(',', expand=True),
        index=expectancy_lg.index
    )

    expectancy_clean = expectancy_lg[expectancy_lg['year'].str.strip().str.isdigit()]
    value_floats = expectancy_clean['value'].str.findall(r"\-?\d+\.\d+")
    expectancy_clean['value'] = pd.to_numeric(value_floats[value_floats.str.len() == 1].str[0])
    expectancy_clean = expectancy_clean.dropna()

    expectancy_pt = expectancy_clean[expectancy_clean['region'] == country]

    expectancy_result = expectancy_pt[['unit', 'sex', 'age', 'region', 'year', 'value']]

    return expectancy_result


def main(country: str='PT') -> None:
    """Loads, cleans and saves data.
    :param country: region where to filter data. 
    """
    expectancy_w = load_data()
    expectancy_result = clean_data(expectancy_w, country)
    save_data(expectancy_result)


if __name__ == "__main__":  # pragma: no cover
    # Country command-line option. (the default should be `PT`)
    parser = argparse.ArgumentParser()
    parser.add_argument("-country", default="PT")
    args = parser.parse_args()

    main(args.country)
