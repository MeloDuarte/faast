"""Tests the read and write module"""
from unittest.mock import patch
import pandas as pd
from life_expectancy.strategies import TSVDataStrategy, JSONDataStrategy, Region, save_data
from . import FIXTURES_DIR, OUTPUT_DIR

def test_read(eu_life_expectancy_sample):
    """
    Run the `load_data` function and compare the output to the expected output
    """
    data = TSVDataStrategy().load_data(FIXTURES_DIR / "eu_life_expectancy_sample.tsv")
    pd.testing.assert_frame_equal(data, eu_life_expectancy_sample)


def test_json_read(eu_life_expectancy_json_sample):
    """
    Run the json `load_data` function and compare the output to the expected output
    """
    data = JSONDataStrategy().load_data(FIXTURES_DIR / "eurostat_life_expect.json")
    pd.testing.assert_frame_equal(data, eu_life_expectancy_json_sample)


def test_write(pt_life_expectancy_expected):
    """
    Run the `save_data` function and checks if the function
    has been called exactly once with specific arguments.
    """
    with patch("pandas.DataFrame.to_csv") as mock_save:
        mock_save.side_effect = print("Saved to csv!!!")
        save_data(pt_life_expectancy_expected)
        mock_save.assert_called_once_with(OUTPUT_DIR / "pt_life_expectancy.csv", index=False)


def test_get_countries(eu_life_countries):
    """
    This test verifies if `get_countries` method in the 
    Region class retrieves only valid countries.
    """
    actual_countries = Region.get_countries()

    assert actual_countries == eu_life_countries
