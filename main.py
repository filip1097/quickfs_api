from analyzer import evaluate_company_soundness

from database_handler import ensure_database_is_initialized
from database_handler import get_best_stock_ticker_to_request
from database_handler import get_companies_with_available_json_data
from database_handler import get_company_row
from database_handler import get_dataset_from_json
from database_handler import store_full_dataset_as_json
from database_handler import store_supported_stocks
from database_handler import update_company_list_db

import dataset_util as ds

from datetime import date

import logging

from quickfs_api import can_get_full_dataset
from quickfs_api import get_all_supported_companies
from quickfs_api import get_full_dataset_from_api


def evaluate_stock_and_update_db(stock_ticker: str, dataset: dict):
    logging.info(f"Before: {get_company_row(stock_ticker)}")
    current_date = date.today().strftime("%Y-%m-%d")
    latest_fiscal_year_date = ds.get_latest_fiscal_year_string(dataset)
    company_soudness = evaluate_company_soundness(dataset)
    update_company_list_db(stock_ticker, current_date, latest_fiscal_year_date, company_soudness)
    logging.info(f"After: {get_company_row(stock_ticker)}")


def main(mode: str):
    logging.basicConfig(filename='quickfs_api.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    ensure_database_is_initialized()

    if mode == 'API':
        request_new_company_info_from_api()
    elif mode == 'REEVALUATE':
        reevalute_companies()


def reevalute_companies():
    companies = get_companies_with_available_json_data()

    for stock_ticker in companies:
        dataset = get_dataset_from_json(stock_ticker)
        evaluate_stock_and_update_db(stock_ticker, dataset)


def request_new_company_info_from_api():
    supported_companies = get_all_supported_companies()
    store_supported_stocks(supported_companies)

    while can_get_full_dataset():
        stock_ticker = get_best_stock_ticker_to_request()
        full_dataset = get_full_dataset_from_api(stock_ticker)
        store_full_dataset_as_json(stock_ticker, full_dataset)
        evaluate_stock_and_update_db(stock_ticker, full_dataset)

    else:
        logging.info("QuickFS API Quota too low.")


if __name__ == '__main__':
    # Available modes:
    # * API
    # * REEVALUATE
    main(mode='REEVALUATE')
