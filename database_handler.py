import json

import sqlite3

JSON_DATA_DIR_PATH = "company_json_data"


def create_company_list_db(cursor):
    company_list_command = """CREATE TABLE company_list (
        company_ticker VARCHAR(20) PRIMARY KEY,
        last_api_get DATE,
        latest_fiscal_year DATE,
        soundness_scrore INTEGER);"""
    cursor.execute(company_list_command)


def does_table_exist(cursor, table_name) -> bool:
    get_tables_command = "SELECT name FROM sqlite_master WHERE type = \"table\";"
    cursor.execute(get_tables_command)
    table_results = cursor.fetchall()

    for table_results_tuple in table_results:
        if table_results_tuple[0] == table_name:
            return True

    return False


def ensure_database_is_initialized():
    """Creates the database tables if they do not already exist."""
    connection = sqlite3.connect("quickfs_api.db")
    cursor = connection.cursor()

    if not does_table_exist(cursor, 'company_list'):
        create_company_list_db(cursor)

    connection.commit()
    connection.close()


def get_company_row(stock_ticker: str):
    connection = sqlite3.connect("quickfs_api.db")
    cursor = connection.cursor()

    select_command = f"SELECT * FROM company_list WHERE company_ticker = \"{stock_ticker}\""
    cursor.execute(select_command)
    company_row = cursor.fetchall()[0]

    connection.commit()
    connection.close()

    return company_row


def get_json_file_name(stock_ticker: str):
    # ':' is not allowed in file names
    stock_ticker_without_colon = stock_ticker.replace(':', '_')
    return f"{stock_ticker_without_colon}.json"


def store_full_dataset_as_json(stock_ticker: str, data: dict):
    file_path = f"{JSON_DATA_DIR_PATH}/{get_json_file_name(stock_ticker)}"
    with open(file_path, 'w') as file:
        file.write(json.dumps(data, indent=2))


def store_supported_stocks(supported_stocks):
    connection = sqlite3.connect("quickfs_api.db")
    cursor = connection.cursor()

    for stock_ticker in supported_stocks:
        select_command = f"SELECT company_ticker FROM company_list WHERE company_ticker = \"{stock_ticker}\""
        cursor.execute(select_command)
        select_result = cursor.fetchall()

        if len(select_result) == 0:
            insert_command = f"INSERT INTO company_list (company_ticker) VALUES (\"{stock_ticker}\");"
            cursor.execute(insert_command)

    connection.commit()
    connection.close()


def update_company_list_db(stock_ticker, last_api_get, latest_fiscal_year, company_soundness):
    connection = sqlite3.connect("quickfs_api.db")
    cursor = connection.cursor()

    select_command = f"SELECT * FROM company_list WHERE company_ticker = \"{stock_ticker}\""
    cursor.execute(select_command)
    company_row = cursor.fetchall()[0]
    company_ticker_in_db, last_api_get_in_db, latest_fiscal_year_in_db, soundness_in_db = company_row

    if stock_ticker != company_ticker_in_db or\
            last_api_get_in_db != last_api_get or\
            latest_fiscal_year_in_db != latest_fiscal_year or\
            soundness_in_db != company_soundness:
        replace_command = f"REPLACE INTO company_list VALUES " \
                          f"(\"{stock_ticker}\", \'{last_api_get}\', \'{latest_fiscal_year}\', {company_soundness});"
        cursor.execute(replace_command)

    connection.commit()
    connection.close()
