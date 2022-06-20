"""Provides helper functions to extract information from a dataset."""
import logging


DATA_IS_NOT_PRESENT_IN_DATASET = ['Data is not present in dataset']
NOT_AVAILABLE = 'N/A'


def get_current_ratio(dataset: dict, n_years: int) -> list:
    current_assets = get_annual_financial_data(dataset, 'total_current_assets', n_years)
    current_liabilities = get_annual_financial_data(dataset, 'total_current_liabilities', n_years)
    if current_assets == DATA_IS_NOT_PRESENT_IN_DATASET or current_liabilities == DATA_IS_NOT_PRESENT_IN_DATASET:
        return DATA_IS_NOT_PRESENT_IN_DATASET

    current_ratio = []
    for c_a, c_l in zip(current_assets, current_liabilities):
        if c_l == 0:
            current_ratio.append(1.5)
        else:
            current_ratio.append(c_a / c_l)

    return current_ratio


def get_annual_financial_data(dataset: dict, data_key: str, n_years=None) -> list:
    if data_key in dataset['data']['financials']['annual']:
        if n_years is None:
            return dataset['data']['financials']['annual'][data_key]
        else:
            return dataset['data']['financials']['annual'][data_key][-n_years:]
    else:
        logging.warning(f"Could not find {data_key} in the dataset.")
        return DATA_IS_NOT_PRESENT_IN_DATASET


def get_debt_to_equity_ratio(dataset: dict, n_years: int) -> list:
    liabilities = get_annual_financial_data(dataset, 'total_liabilities', n_years)
    equity = get_annual_financial_data(dataset, 'total_equity', n_years)
    if liabilities == DATA_IS_NOT_PRESENT_IN_DATASET or equity == DATA_IS_NOT_PRESENT_IN_DATASET:
        return DATA_IS_NOT_PRESENT_IN_DATASET

    debt_to_equity = []
    for lia, e in zip(liabilities, equity):
        debt_to_equity.append(lia / e)

    return debt_to_equity


def get_eps(dataset: dict, n_years: int) -> list:
    net_income = get_annual_financial_data(dataset, 'net_income', n_years)
    pref_divididends = get_annual_financial_data(dataset, 'preferred_dividends', n_years)
    n_shares = get_annual_financial_data(dataset, 'shares_diluted', n_years)
    if net_income == DATA_IS_NOT_PRESENT_IN_DATASET or \
            pref_divididends == DATA_IS_NOT_PRESENT_IN_DATASET or \
            n_shares == DATA_IS_NOT_PRESENT_IN_DATASET:
        return DATA_IS_NOT_PRESENT_IN_DATASET

    if any([n_s == 0 for n_s in n_shares]):
        logging.warning("Company has 0 shares diluted")
        return DATA_IS_NOT_PRESENT_IN_DATASET

    eps = []
    for n_i, p_d, n_s in zip(net_income, pref_divididends, n_shares):
        eps.append((n_i - p_d) / n_s)

    return eps


def get_equity(dataset: dict, n_years: int) -> list:
    equity = get_annual_financial_data(dataset, 'total_equity', n_years)
    if equity == DATA_IS_NOT_PRESENT_IN_DATASET:
        return DATA_IS_NOT_PRESENT_IN_DATASET

    return equity


def get_fcf(dataset: dict, n_years: int) -> list:
    # Maybe this should be calculated?
    fcf = get_annual_financial_data(dataset, 'fcf', n_years)
    if fcf == DATA_IS_NOT_PRESENT_IN_DATASET:
        return DATA_IS_NOT_PRESENT_IN_DATASET

    return fcf


def get_fiscal_years(dataset: dict) -> list:
    fiscal_years = get_annual_financial_data(dataset, 'fiscal_year_number')
    if fiscal_years == DATA_IS_NOT_PRESENT_IN_DATASET:
        return DATA_IS_NOT_PRESENT_IN_DATASET

    return fiscal_years


def get_latest_fiscal_year_string(dataset: dict) -> str:
    fiscal_years = get_annual_financial_data(dataset, 'fiscal_year_number', 1)
    if fiscal_years == DATA_IS_NOT_PRESENT_IN_DATASET:
        return NOT_AVAILABLE

    latest_fiscal_year = fiscal_years[0]
    return f"{latest_fiscal_year}-01-01"
