"""Tests for the cleaning module"""
from unittest.mock import patch
import pandas as pd
from life_expectancy.strategies import TSVDataStrategy, JSONDataStrategy, Region
from life_expectancy.cleaning import main, MainCleaning
from . import FIXTURES_DIR

def test_clean_data(pt_life_expectancy_expected, eu_life_expectancy_sample):
    """
    Run the `clean_data` function on a sample dataframe and
    compare the output to the expected output
    """

    tsv_strategy = TSVDataStrategy()
    tsv_strategy.expectancy = eu_life_expectancy_sample
    pt_life_expectancy_actual = tsv_strategy.clean_data()
    pt_life_expectancy_actual = pt_life_expectancy_actual.reset_index(drop=True)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )


def test_json_clean_data(pt_life_expectancy_json_expected, eu_life_expectancy_json_sample):
    """
    Run the json `clean_data` function on a sample dataframe and
    compare the output to the expected output
    """
    json_strategy = JSONDataStrategy()
    json_strategy.expectancy = eu_life_expectancy_json_sample
    pt_life_expectancy_actual = json_strategy.clean_data()
    pt_life_expectancy_actual = pt_life_expectancy_actual.reset_index(drop=True)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_json_expected
    )


def test_main(pt_life_expectancy_expected):
    """
    Run the `main` function on a sample dataframe and
    compare the output to the expected output
    """

    filename = FIXTURES_DIR / "eu_life_expectancy_sample.tsv"
    
    main_instance = MainCleaning(filename, TSVDataStrategy(), Region.PT)

    # Mock the read and write functions and assert the expected results
    with patch('life_expectancy.cleaning.MainCleaning', return_value=main_instance), \
         patch('life_expectancy.cleaning.save_data', side_effect=print("Saved to csv!!!")):

        pt_life_expectancy_actual = main(country=Region.PT).reset_index(drop=True)
        print(f"the result{pt_life_expectancy_actual}")
        pd.testing.assert_frame_equal(
                pt_life_expectancy_actual, pt_life_expectancy_expected
        )
