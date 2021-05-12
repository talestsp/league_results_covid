import pandas as pd
import urllib.request
from src.utils import datetime_utils
from src.dao import make_dirs

COUNTRY_DATA_FILENAME_MAP = {"SPAIN": "SP1",
                             "ENGLAND": "E0",
                             "ITALY": "I1",
                             "PORTUGAL": "P1",
                             "NETHERLANDS": "N1",
                             "GERMANY": "D1",
                             "FRANCE": "F1"}

RAW_DATA_DIR = "data/raw/"

def raw_data_filepath(country, season):
    return f'{RAW_DATA_DIR}{country.lower()}/{country.lower()}_{season[0]}_{season[1]}.csv'

def load_season_data(filepath):
    '''
    Load a CSV as a pandas.DataFrame
    :param filepath: CSV path to be loaded
    :return:
    '''
    season_data = pd.read_csv(filepath)
    season_data["Date"] = season_data["Date"].apply(datetime_utils.date_str_to_datetime)

    return season_data.sort_values(["Date", "HomeTeam"]).reset_index(drop=True)

def load_league_data(season: str, country: str):
    '''
    Load a previous stored season matches data.
    :param season: String representing the season in format 'YEAR1/YEAR2'
    :param country: Name of the country.
    :return: A pandas.DataFrame with all team matches.
    '''
    filepath = raw_data_filepath(country, season)
    season_data = load_season_data(filepath)
    season_name = f"{season[0]}/{season[1]}"
    season_data["Season"] = season_name
    return season_data

def download_data(country: str, seasons: str):
    '''
    It downloads country's season matches data from www.football-data.co.uk website.
    I apreciatte the effort of the football-data.co.uk team in order to make these datasets available and
    constantly updated. Thank you very much. :)
    :param country: Name of the country. Please check keys from COUNTRY_DATA_FILENAME_MAP.
    :param season: String representing the season in format 'YEAR1/YEAR2'
    :return:
    '''
    make_dirs.mk_general_data_dir()
    make_dirs.mkdir(RAW_DATA_DIR)
    filename = COUNTRY_DATA_FILENAME_MAP[country.upper()]
    make_dirs.mkdir(RAW_DATA_DIR + country.lower())

    for season in seasons:
        print(country.upper(), "{} / {}".format(season[0], season[1]))
        url = "http://www.football-data.co.uk/mmz4281/{}{}/{}.csv".format(season[0], season[1], filename)
        urllib.request.urlretrieve(url, raw_data_filepath(country, season))
