"""Tests for the cleaning module"""
from unittest.mock import patch
import pandas as pd
from life_expectancy.cleaning import clean_data, main

def test_clean_data(pt_life_expectancy_expected, eu_life_expectancy_sample):
    """Run the `clean_data` function and compare the output to the expected output"""

    pt_life_expectancy_actual = clean_data(eu_life_expectancy_sample)
    pt_life_expectancy_actual = pt_life_expectancy_actual.reset_index(drop=True)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )


def test_main(eu_life_expectancy_sample, pt_life_expectancy_expected):
    """Run the `main` function and compare the output to the expected output"""
    # Mock the read and write functions and assert the expected results
    with patch('life_expectancy.cleaning.load_data', return_value=eu_life_expectancy_sample), \
         patch('life_expectancy.cleaning.save_data', side_effect=print("Saved to csv!!!")):

        pt_life_expectancy_actual = main(country='PT').reset_index(drop=True)

        pd.testing.assert_frame_equal(
                pt_life_expectancy_actual, pt_life_expectancy_expected
        )
