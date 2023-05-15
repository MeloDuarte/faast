"""Module for loading/saving data"""
from pathlib import Path
import pandas as pd
from pandas import DataFrame

def load_data(filename: str) -> DataFrame:
    """
    Loads `eu_life_expectancy_raw.tsv` DataFrame.
    :filename: path to the load file.
    :return: DataFrame loaded.
    """
    data = pd.read_csv(
        filename,
        sep='\t',
        header=0
    )

    return data


def save_data(expectancy_result: DataFrame) -> None:
    """
    Save the resulting DataFrame to `pt_life_expectancy.csv`.
    :param expectancy_result: DataFrame cleaned to be saved.
    """
    # Gives the parent dir location of the file `pt_life_expectancy.csv`
    filename = Path(__file__).parent / "data/pt_life_expectancy.csv"
    print(filename)

    expectancy_result.to_csv(
        filename,
        index=False
    )
