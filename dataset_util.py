"""Provides helper functions to extract information from a dataset."""


def get_current_ratio(dataset: dict, n_years: int) -> list:
    current_assets = dataset['data']['financials']['annual']['total_current_assets'][n_years:]
    current_liabilities = dataset['data']['financials']['annual']['total_current_liabilities'][n_years:]

    current_ratio = []
    for c_a, c_l in zip(current_assets, current_liabilities):
        current_ratio.append(c_a / c_l)

    return current_ratio


def get_debt_to_equity_ratio(dataset: dict, n_years: int) -> list:
    liabilities = dataset['data']['financials']['annual']['total_liabilities'][n_years:]
    equity = dataset['data']['financials']['annual']['total_equity'][n_years:]

    debt_to_equity = []
    for l, e in zip(liabilities, equity):
        debt_to_equity.append(l / e)

    return debt_to_equity


def get_eps(dataset: dict, n_years: int) -> list:
    net_income = dataset['data']['financials']['annual']['net_income'][n_years:]
    pref_divididends = dataset['data']['financials']['annual']['preferred_dividends'][n_years:]
    n_shares = dataset['data']['financials']['annual']['shares_diluted'][n_years:]

    eps = []
    for n_i, p_d, n_s in zip(net_income, pref_divididends, n_shares):
        eps.append((n_i - p_d) / n_s)

    return eps


def get_equity(dataset: dict, n_years: int) -> list:
    equity = dataset['data']['financials']['annual']['total_equity'][n_years:]
    return equity


def get_fcf(dataset: dict, n_years: int) -> list:
    # Maybe this should be calculated?
    fcf = dataset['data']['financials']['annual']['fcf'][n_years:]
    return fcf


def get_latest_fiscal_year_string(dataset: dict) -> str:
    latest_fiscal_year = dataset['data']['financials']['annual']['fiscal_year_number'][-1]
    return f"{latest_fiscal_year}-01-01"


def get_number_of_fiscal_years_available(dataset: dict) -> int:
    return len(dataset['data']['financials']['annual']['fiscal_year_number'])
