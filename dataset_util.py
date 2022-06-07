"""Provides helper functions to extract information from a dataset."""


def get_latest_fiscal_year_string(dataset: dict) -> str:
    latest_fiscal_year = dataset['data']['financials']['annual']['fiscal_year_number'][-1]
    return f"{latest_fiscal_year}-01-01"
