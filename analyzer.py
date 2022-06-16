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


def calc_soundness_from_equity(equity: list):
    total_years = len(equity)
    if total_years == 1:
        return 0
    else:
        growing_years = len([1 for i in range(len(equity) - 1) if equity[i + 1] - equity[i] > 0])
        return 100 * growing_years / (total_years - 1)


def calc_soundness_from_num_fiscal_years(number_of_years: int):
    if number_of_years >= 10:
        return 100
    else:
        return 100 * number_of_years / 10


def calc_soundness_from_eps_or_fcf(eps_or_fcf: list):
    total_years = len(eps_or_fcf)
    profitable_years = len([val for val in eps_or_fcf if val > 0])
    if total_years == 1:
        return 100 * profitable_years / total_years
    else:
        growing_years = len([1 for i in range(len(eps_or_fcf) - 1) if eps_or_fcf[i + 1] - eps_or_fcf[i] > 0])
        return 100 * (profitable_years / total_years + growing_years / (total_years - 1))


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
    company_soundness += calc_soundness_from_eps_or_fcf(eps)
    company_soundness += calc_soundness_from_eps_or_fcf(fcf)

    # 2.1 Debt-to-Equity ratio < 1.0 (Pref < 0.5)
    company_soundness += calc_soundness_from_debt_to_equity(debt_to_equity[0])

    # 2.2 Current Ratio > 1.0 (Pref > 1.5)
    company_soundness += calc_soundness_from_current_ratio(current_ratio[0])

    # 3 Equity is growing over time
    company_soundness += calc_soundness_from_equity(equity)

    return round(company_soundness, 0)
