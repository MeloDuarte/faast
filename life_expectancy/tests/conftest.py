"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")

@pytest.fixture
def eu_life_expectancy_sample() -> pd.DataFrame:
    """Fixture to load a sample of the raw life expectancy data"""
    data = pd.read_csv(
        FIXTURES_DIR / "eu_life_expectancy_sample.tsv",
        sep="\t",
        header=0
    )
    return data

@pytest.fixture
def eu_life_countries() -> list:
    """Fixture to load list of countries available in life expectancy data"""
    countries = [
        'AT',
        'BE',
        'BG',
        'CH', 
        'CY', 
        'CZ', 
        'DK', 
        'EE', 
        'EL', 
        'ES', 
        'FI', 
        'FR',
        'HR', 
        'HU', 
        'IS',
        'IT',
        'LI',
        'LT',
        'LU',
        'LV',
        'MT',
        'NL',
        'NO',
        'PL',
        'PT',
        'RO',
        'SE', 
        'SI', 
        'SK',
        'DE', 
        'AL',
        'IE', 
        'ME', 
        'MK',
        'RS', 
        'AM', 
        'AZ', 
        'GE', 
        'TR', 
        'UA', 
        'BY', 
        'UK',
        'XK',
        'FX',
        'MD',
        'SM',
        'RU'
    ]
    return countries
