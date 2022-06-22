import logging

import dataset_util as ds


def calc_soundness_from_current_ratio(current_ratio: float):
    distance_from_best_current_ratio = abs(1.5 - current_ratio)
    if distance_from_best_current_ratio > 1:
        return 0
    else:
        return 100 * (1 - distance_from_best_current_ratio)


def calc_soundness_from_debt_to_equity(debt_to_equity: float):
    if debt_to_equity > 2 or debt_to_equity < 0:
        return 0
    else:
        return 100 * (2 - debt_to_equity)


def calc_soundness_from_num_fiscal_years(number_of_years: int):
    if number_of_years >= 10:
        return 100
    else:
        return 100 * number_of_years / 10


def evaluate_company_soundness(full_dataset: dict) -> int:
    """Calculates the 'soundness' of a company based on the provided data set.

    Maximum soundness is: 900
    """
    company_soundness = 0

    fiscal_years = ds.get_fiscal_years(full_dataset)
    if fiscal_years == ds.DATA_IS_NOT_PRESENT_IN_DATASET:
        return -1

    number_of_years = min(len(fiscal_years), 10)
    eps = ds.get_eps(full_dataset, number_of_years)
    fcf = ds.get_fcf(full_dataset, number_of_years)
    debt_to_equity = ds.get_debt_to_equity_ratio(full_dataset, 1)
    current_ratio = ds.get_current_ratio(full_dataset, 1)
    equity = ds.get_equity(full_dataset, number_of_years)

    if eps == ds.DATA_IS_NOT_PRESENT_IN_DATASET or \
            fcf == ds.DATA_IS_NOT_PRESENT_IN_DATASET or \
            debt_to_equity == ds.DATA_IS_NOT_PRESENT_IN_DATASET or \
            current_ratio == ds.DATA_IS_NOT_PRESENT_IN_DATASET or \
            equity == ds.DATA_IS_NOT_PRESENT_IN_DATASET:
        return -1

    # 1.1 Number of years of data available
    company_soundness += calc_soundness_from_num_fiscal_years(number_of_years)

    # 1.2 Profitable every year terms of EPS and FCF
    # 1.3 EPS and FCF are growing over time
    company_soundness += get_soundness(eps, above_limit=0, growing=True)
    company_soundness += get_soundness(fcf, above_limit=0, growing=True)
    print(company_soundness)

    # 2.1 Debt-to-Equity ratio < 1.0 (Pref < 0.5)
    company_soundness += calc_soundness_from_debt_to_equity(debt_to_equity[0])

    # 2.2 Current Ratio > 1.0 (Pref > 1.5)
    company_soundness += calc_soundness_from_current_ratio(current_ratio[0])

    # 3 Equity is growing over time
    company_soundness += get_soundness(fcf, growing=True)

    return round(company_soundness, 0)


def get_soundness(values: list, above_limit=None, calc_distance=False, growing=False):
    soundness = 0
    num_years = len(values)

    if above_limit is not None:
        if calc_distance:
            distances = []
            for val in values:
                if val <
        else:
            num_years_above_limit = len([val for val in values if val > 0])
            soundness += 100 * num_years_above_limit / num_years


    if growing and num_years > 1:
        growing_years = len([1 for i in range(len(values) - 1) if values[i + 1] - values[i] > 0])
        soundness += 100 * growing_years / (num_years - 1)

    return soundness
