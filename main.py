from analyzer import evaluate_company_soundness

from database_handler import ensure_database_is_initialized
from database_handler import get_company_row
from database_handler import store_full_dataset_as_json
from database_handler import store_supported_stocks
from database_handler import update_company_list_db

import dataset_util as ds

from datetime import date

import logging

from quickfs_api import can_get_full_dataset
from quickfs_api import get_all_supported_companies
from quickfs_api import get_full_dataset


def gen_latest_fiscal_year_string(full_dataset: dict) -> str:
    latest_fiscal_year = full_dataset['data']['financials']['annual']['fiscal_year_number'][-1]
    return f"{latest_fiscal_year}-01-01"


def main():
    logging.basicConfig(filename='quickfs_api.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    ensure_database_is_initialized()
    supported_companies = get_all_supported_companies()
    store_supported_stocks(supported_companies)

    if can_get_full_dataset():
        stock_ticker = 'AAPL:US'
        full_dataset = get_full_dataset(stock_ticker)
        store_full_dataset_as_json(stock_ticker, full_dataset)

        current_date = date.today().strftime("%Y-%m-%d")
        latest_fiscal_year_date = ds.get_latest_fiscal_year_string(full_dataset)
        company_soudness = evaluate_company_soundness(full_dataset)
        update_company_list_db(stock_ticker, current_date, latest_fiscal_year_date, company_soudness)

    else:
        logging.info("QuickFS API Quota too low.")


if __name__ == '__main__':
    main()
