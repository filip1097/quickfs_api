import dataset_util as ds

import math


def calc_soundness_from_current_ratio(current_ratio: float):
    distance_from_best_current_ratio = abs(1.5 - current_ratio)
    if distance_from_best_current_ratio > 1:
        return 0
    else:
        return 200 * distance_from_best_current_ratio


def calc_soundness_from_debt_to_equity(debt_to_equity: float):
    if debt_to_equity > 2 or debt_to_equity < 0:
        return 0
    else:
        return 100 * (2 - debt_to_equity)


def calc_soundness_from_equity(equity: list):
    total_years = len(equity)
    growing_years = len([1 for i in range(len(equity) - 1) if equity[i + 1] - equity[i] > 0])
    return math.sin(math.pi / 2 * growing_years / total_years)


def calc_soundness_from_num_fiscal_years(number_of_years: int):
    if number_of_years >= 10:
        return 100
    else:
        return math.sin(math.pi / 2 * number_of_years / 10)


def calc_soundness(vals: list):
    total_years = len(vals)
    profitable_years = len([val for val in vals if val > 0])
    growing_years = len([1 for i in range(len(vals) - 1) if vals[i + 1] - vals[i] > 0])
    return math.sin(math.pi / 2 * profitable_years / total_years) + \
        math.sin(math.pi / 2 * growing_years / total_years)


def evaluate_company_soundness(full_dataset: dict) -> int:
    company_soundness = 0

    # 1.1 Get number of years of data available
    number_of_years = min(ds.get_number_of_fiscal_years_available(full_dataset), 10)
    company_soundness += calc_soundness_from_num_fiscal_years(number_of_years)

    # 1.2 Profitable every year terms of EPS and FCF
    # 1.3 EPS and FCF are growing over time
    eps = ds.get_eps(full_dataset, number_of_years)
    fcf = ds.get_fcf(full_dataset, number_of_years)
    company_soundness += calc_soundness(eps)
    company_soundness += calc_soundness(fcf)

    # 2.1 Debt-to-Equity ratio < 1.0 (Pref < 0.5)
    debt_to_equity = ds.get_debt_to_equity_ratio(full_dataset, 1)[0]
    company_soundness += calc_soundness_from_debt_to_equity(debt_to_equity)

    # 2.2 Current Ratio > 1.0 (Pref > 1.5)
    current_ratio = ds.get_current_ratio(full_dataset, 1)[0]
    company_soundness += calc_soundness_from_current_ratio(current_ratio)

    # 3 Equity is growing over time
    equity = ds.get_equity(full_dataset, number_of_years)
    company_soundness += calc_soundness_from_equity(equity)

    return company_soundness
