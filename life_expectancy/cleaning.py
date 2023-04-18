"""Module Assignment 1: EU Life Expectancy"""

import argparse
import pandas as pd

def clean_data(country):
    """
    Loads `eu_life_expectancy_raw.tsv` dataframe and cleans it.
    Save the resulting dataframe to `pt_life_expectancy.csv`.
    """
    expectancy_w = pd.read_csv(
        "life_expectancy/data/eu_life_expectancy_raw.tsv",
        sep='\t',
        header=0
    )

    expectancy_lg = pd.melt(expectancy_w, id_vars=expectancy_w.columns[0], var_name="year")

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
    expectancy_result.to_csv('life_expectancy/data/pt_life_expectancy.csv', index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("-country", default="PT")
    args = parser.parse_args()
    clean_data(args.country)
