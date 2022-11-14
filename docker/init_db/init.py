# -*- coding: utf-8 -*-

# Standard modules
import os
import csv
import json
import configparser
from typing import Final, List, Tuple
from contextlib import closing

# Third-party modules
import psycopg2
import psycopg2.extras
from psycopg2 import Error

config = configparser.ConfigParser(allow_no_value=True)
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
    dict_obj = json.load(f)
config.read_dict(dict_obj)
DB_USER: Final[str] = config.get("database", "user")
DB_PASSWORD: Final[str] = config.get("database", "password")
DB_HOST_ALIAS: Final[str] = config.get("database", "host_alias")
DB_PORT: Final[str] = config.get("database", "port")
DB_NAME: Final[str] = config.get("database", "database")
FILE_DIR: Final[str] = config.get("file", "file_dir")
FILE_NAME: Final[str] = config.get("file", "file_name")

FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), FILE_DIR, FILE_NAME)


def check_db(cursor, true_values: List[Tuple[str, str]]) -> bool:
    cursor.execute("SELECT name, age from data;")
    for response_row, request_row in zip(cursor, true_values):
        if response_row[0] != request_row[0] or response_row[1] != int(request_row[1]):
            return False
    return True


def fill_db(db_user: str, db_password: str, db_host: str, db_port: str, db: str, path: str) -> None:
    try:
        print("Starting initialization of database!")
        with closing(
                psycopg2.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=db)) as conn:
            with conn, conn.cursor() as cursor:  # cursor_factory=psycopg2.extras.DictCursor) as cursor:
                conn.autocommit = True
                cursor.execute("""
                CREATE TABLE data (
                id      SERIAL PRIMARY KEY,
                name    varchar(250),
                age     integer
                );""")

                with open(path) as csv_f:
                    reader = csv.reader(csv_f, delimiter=",")
                    values = [(row[0], row[1]) for row in reader]

                    records_list_template = ','.join(['%s'] * len(values))
                    insert = 'INSERT INTO data (name, age) VALUES {}'.format(records_list_template)
                    cursor.execute(insert, values)

                    print(cursor.statusmessage)

                if check_db(cursor, values):
                    print("Database has successfully initialiazed!")
                else:
                    print("Database is initialized not correct!")
    except (Exception, Error) as err:
        print("Some errors occured while initialiazing database!\nError: ", err)


if __name__ == "__main__":
    fill_db(DB_USER, DB_PASSWORD, DB_HOST_ALIAS, DB_PORT, DB_NAME, FILE_PATH)
