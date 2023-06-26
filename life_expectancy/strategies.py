"""Module for loading/saving data"""
from pathlib import Path
from typing import List
from enum import Enum
from abc import ABC, abstractmethod
import pandas as pd
from pandas import DataFrame


class Region(Enum):
    """
    Possible regions in life expectancy data.
    """
    AT = 'AT'
    BE = 'BE'
    BG = 'BG'
    CH = 'CH'
    CY = 'CY'
    CZ = 'CZ'
    DK = 'DK'
    EE = 'EE'
    EL = 'EL'
    ES = 'ES'
    EU27_2020 = 'EU27_2020'
    FI = 'FI'
    FR = 'FR'
    HR = 'HR'
    HU = 'HU'
    IS = 'IS'
    IT = 'IT'
    LI = 'LI'
    LT = 'LT'
    LU = 'LU'
    LV = 'LV'
    MT = 'MT'
    NL = 'NL'
    NO = 'NO'
    PL = 'PL'
    PT = 'PT'
    RO = 'RO'
    SE = 'SE'
    SI = 'SI'
    SK = 'SK'
    DE = 'DE'
    DE_TOT = 'DE_TOT'
    AL = 'AL'
    EA18 = 'EA18'
    EA19 = 'EA19'
    EFTA = 'EFTA'
    IE = 'IE'
    ME = 'ME'
    MK = 'MK'
    RS = 'RS'
    AM = 'AM'
    AZ = 'AZ'
    GE = 'GE'
    TR = 'TR'
    UA = 'UA'
    BY = 'BY'
    EEA30_2007 = 'EEA30_2007'
    EEA31 = 'EEA31'
    EU27_2007= 'EU27_2007'
    EU28 = 'EU28'
    UK = 'UK'
    XK = 'XK'
    FX = 'FX'
    MD = 'MD'
    SM = 'SM'
    RU = 'RU'

    @classmethod
    def get_countries(cls) -> List[str]:
        """
        Filters valid countries.
        :return: A list of region codes representing valid countries.
        """
        not_countries = [
            'EU27_2020',
            'DE_TOT',
            'EA18',
            'EA19',
            'EFTA',
            'EEA30_2007',
            'EEA31',
            'EU27_2007',
            'EU28'
        ]
        countries = [country.value for country in cls if country.value not in not_countries]
        return countries


class DataStrategy(ABC):
    """
    Abstract base class for data loading and cleaning strategies.
    """
    @abstractmethod
    def load_data(self, filename: str) -> DataFrame:
        """
        Loads `eu_life_expectancy_raw.tsv` DataFrame.
        """

    @abstractmethod
    def clean_data(self, country: Region = Region.PT) -> DataFrame:
        """
        Cleans data to the required format.
        """

class TSVDataStrategy(DataStrategy):
    """
    Loads data from a TSV file and returns cleaned life expectancy dataframe.
    """
    def __init__(self):
        self.expectancy = None

    def load_data(self, filename: str) -> DataFrame:
        """
        Loads data from a TSV file and returns a pandas dataframe.
        :param filename: The path to the TSV file to load.
        :return: The loaded data as a pandas DataFrame.
        """
        data = pd.read_csv(
                filename,
                sep='\t',
                header=0
        )

        self.expectancy = data
        return data

    def clean_data(self, country: Region = Region.PT) -> DataFrame:
        """
        Unpivots the DataFrame to long format, ensures `year` is an `int`
        (with the appropriate data cleaning if required), ensures `value`
        is a `float` (with the appropriate data cleaning if required, 
        and do remove the NaNs) and filters the data by region.
        :param country: region where to filter data.
        :return: cleaned DataFrame
        """
        self.expectancy = self._unpivot_data()
        self.expectancy = self._filter_by_region(country.value)
        self.expectancy = self._ensure_column_quality()

        self.expectancy = self.expectancy[['unit', 'sex', 'age', 'region', 'year', 'value']]

        return self.expectancy

    def _unpivot_data(self) -> DataFrame:
        # Unpivot the DataFrame to long format
        expectancy_lg = pd.melt(
            self.expectancy,
            id_vars=self.expectancy.columns[0],
            var_name="year"
        )
        expectancy_lg[['unit', 'sex', 'age', 'region']] = pd.DataFrame(
            expectancy_lg[expectancy_lg.columns[0]].str.split(',', expand=True),
            index=expectancy_lg.index
        )
        return expectancy_lg

    def _ensure_column_quality(self) -> DataFrame:
        # Find all occurrences of floats in column `value`
        # and converts argument to numeric type. Returns NaN otherwise.
        expectancy_clean = self.expectancy[self.expectancy['year'].str.strip().str.isdigit()]

        value_floats = expectancy_clean['value'].str.findall(r"\-?\d+\.\d+")
        expectancy_clean['value'] = pd.to_numeric(value_floats[value_floats.str.len() == 1].str[0])

        # Drops all NaN rows in columns `year` and `value`
        expectancy_clean = expectancy_clean.dropna(subset=['year', 'value'])

        expectancy_clean['year'] = expectancy_clean['year'].astype(int)
        return expectancy_clean

    def _filter_by_region(self, region: str) -> DataFrame:
        # Filter the data by region
        expectancy_region = self.expectancy[self.expectancy['region'].str.upper() == region.upper()]
        return expectancy_region


class JSONDataStrategy(DataStrategy):
    """
    Loads data from a JSON file and returns cleaned life expectancy dataframe.
    """
    def __init__(self):
        self.expectancy = None

    def load_data(self, filename: str) -> DataFrame:
        """
        Loads data from a JSON file and returns a pandas dataframe.
        :param filename: The path to the JSON file to load.
        :return: The loaded data as a pandas DataFrame.
        """
        data = pd.read_json(
                filename
        )
        self.expectancy = data
        return data

    def clean_data(self, country: Region = Region.PT) -> DataFrame:
        """
        Filters the data by the specified region,
        renames relevant columns, and drops unnecessary columns
        :param expectancy: expectancy DataFrame in wide format.
        :param country: region where to filter data.
        :return: cleaned DataFrame
        """
        expectancy_region = self.expectancy[
            self.expectancy['country'].str.upper() == country.value.upper()
        ]

        expectancy_region = expectancy_region.rename(
            columns={"country": "region", "life_expectancy": "value"}
        )

        expectancy_result = expectancy_region.drop(columns=["flag", "flag_detail"])

        return expectancy_result


def save_data(expectancy_result: DataFrame) -> None:
    """
    Save the resulting DataFrame to `pt_life_expectancy.csv`.
    :param expectancy_result: DataFrame cleaned to be saved.
    """
    # Gives the parent dir location of the file `pt_life_expectancy.csv`
    filename = Path(__file__).parent / "data/pt_life_expectancy.csv"

    expectancy_result.to_csv(
        filename,
        index=False
    )
