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
    logging.info(f"Get list of supported companies, country code: {country}, exchange: {exchange}")
    url = f"{API_URL_BASE}/companies/{country}/{exchange}"
    response = requests.get(url, headers=gen_header())

    if response.status_code == 200:
        return response.json()['data']
    else:
        print_error_status_code(response)
        return []


def get_full_dataset_from_api(company_ticker: str) -> dict:
    logging.info(f"Get full dataset for {company_ticker}")
    url = f"{API_URL_BASE}/data/all-data/{company_ticker}"
    response = requests.get(url, headers=gen_header())

    if response.status_code == 200:
        return response.json()
    else:
        print_error_status_code(response)
        return {}


def get_remaining_api_quota() -> int:
    logging.info("Get remaining API quota.")
    url = f"{API_URL_BASE}/usage"
    response = requests.get(url, headers=gen_header())

    if response.status_code == 200:
        return response.json()['usage']['quota']['remaining']
    else:
        print_error_status_code(response)
        return -1


def print_error_status_code(response):
    r_json = response.json()
    logging.error(f"Status code: <{r_json['status']}> | {r_json['error']} | {r_json['description']}")
