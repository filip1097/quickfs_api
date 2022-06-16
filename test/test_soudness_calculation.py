import unittest

from analyzer import evaluate_company_soundness


class TestSoundnessCalculation(unittest.TestCase):

    def test_good_soundness(self):
        # define good dataset
        dataset = {
            'data': {
                'financials': {
                    'annual': {
                        'fiscal_year_number': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
                        'net_income': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        'preferred_dividends': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'shares_diluted': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        'fcf': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        'total_liabilities': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                        'total_equity': [91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
                        'total_current_assets': [15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
                        'total_current_liabilities': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
                    }
                }
            }
        }

        soundness = evaluate_company_soundness(dataset)
        self.assertEqual(890, soundness)

    def test_bad_soundness(self):
        # define bad dataset
        dataset = {
            'data': {
                'financials': {
                    'annual': {
                        'fiscal_year_number': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
                        'net_income': [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10],
                        'preferred_dividends': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'shares_diluted': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        'fcf': [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10],
                        'total_liabilities': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                        'total_equity': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                        'total_current_assets': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        'total_current_liabilities': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
                    }
                }
            }
        }

        soundness = evaluate_company_soundness(dataset)
        self.assertEqual(100, soundness)
