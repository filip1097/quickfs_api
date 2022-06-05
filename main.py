from database_handler import ensure_database_is_initialized
from database_handler import store_supported_stocks

from quickfs_api import can_get_full_dataset
from quickfs_api import get_all_supported_companies
from quickfs_api import get_full_dataset


def main():
    ensure_database_is_initialized()
    supported_companies = get_all_supported_companies()
    store_supported_stocks(supported_companies)

    if can_get_full_dataset():
        json_response = get_full_dataset('AAPL:US')
        print(json_response)


if __name__ == '__main__':
    main()
