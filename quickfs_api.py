import logging
import requests

API_URL_BASE = "https://public-api.quickfs.net/v1"

COUNTRY_NAME_FOR_COUNTRY_CODE = {'US': 'United States',
                                 'CA': 'Canada',
                                 'AU': 'Australia',
                                 'NZ': 'New Zealand',
                                 'MM': 'Mexico',
                                 'LN': 'London'}

EXCHANGES_FOR_COUNTRY_CODE = {'US': ['NYSE', 'NASDAQ', 'OTC', 'NYSEARCA', 'BATS', 'NYSEAMERICAN'],
                              'CA': ['TORONTO', 'CSE', 'TSXVENTURE'],
                              'AU': ['ASX'],
                              'NZ': ['NZX'],
                              'MM': ['BMV'],
                              'LN': ['LONDON']}

GET_FULL_DATASET_QUOTA_COST = 10

SUPPORTED_COUNTRY_CODES = ['US', 'CA', 'AU', 'NZ', 'MM', 'LN']


def can_get_full_dataset():
    return get_remaining_api_quota() >= GET_FULL_DATASET_QUOTA_COST


def gen_header() -> dict:
    with open('API_KEY', 'r') as file:
        api_key = file.read()

    header = {'x-qfs-api-key': api_key}

    return header


def get_all_supported_companies() -> list:
    companies = []
    for country_code in SUPPORTED_COUNTRY_CODES:
        for exchange in EXCHANGES_FOR_COUNTRY_CODE[country_code]:
            companies += get_list_of_supported_companies(country_code, exchange)

    # remove any duplicates
    return list(set(companies))


def get_list_of_supported_companies(country: str, exchange: str) -> list:
    logging.info("Get list of supported companies, country code: {}, exchange: {}".format(country, exchange))
    url = "{}/companies/{}/{}".format(API_URL_BASE, country, exchange)
    return requests.get(url, headers=gen_header()).json()['data']


def get_full_dataset(company_ticker: str) -> dict:
    logging.info("Get full dataset for {}.".format(company_ticker))
    url = "{}/data/all-data/{}".format(API_URL_BASE, company_ticker)
    return requests.get(url, headers=gen_header()).json()


def get_remaining_api_quota() -> int:
    logging.info("Get remaining API quota.")
    url = "{}/usage".format(API_URL_BASE)
    return requests.get(url, headers=gen_header()).json()['usage']['quota']['remaining']
