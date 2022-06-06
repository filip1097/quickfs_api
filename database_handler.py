import json

import sqlite3

JSON_DATA_DIR_PATH = "company_json_data"


def create_company_list_db(cursor):
    company_list_command = """CREATE TABLE company_list (
        company_ticker VARCHAR(20) PRIMARY KEY,
        last_api_get DATE,
        last_financial_year DATE,
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


def store_full_dataset_as_json(stock_ticker: str, data: dict):
    file_path = "{}/{}.json".format(JSON_DATA_DIR_PATH, stock_ticker.replace(':', '_'))
    with open(file_path, 'w') as file:
        file.write(json.dumps(data))


def store_supported_stocks(supported_stocks):
    connection = sqlite3.connect("quickfs_api.db")
    cursor = connection.cursor()

    for stock_ticker in supported_stocks:
        select_command = "SELECT company_ticker FROM company_list WHERE company_ticker = \"{}\"".format(stock_ticker)
        cursor.execute(select_command)
        select_result = cursor.fetchall()

        if len(select_result) == 0:
            insert_command = "INSERT INTO company_list (company_ticker) VALUES (\"{}\");".format(stock_ticker)
            cursor.execute(insert_command)

    connection.commit()
    connection.close()
