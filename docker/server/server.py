# -*- coding: utf-8 -*-

# Standard modules
import os
import json
import configparser
from typing import Final
from contextlib import closing

# Third-party modules
import psycopg2
from psycopg2.extras import DictCursor
import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

config = configparser.ConfigParser(allow_no_value=True)
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8") as f:
    dict_obj = json.load(f)
config.read_dict(dict_obj)
DB_USER: Final[str] = config.get("database", "user")
DB_PASSWORD: Final[str] = config.get("database", "password")
DB_HOST_ALIAS: Final[str] = config.get("database", "host_alias")
DB_PORT: Final[str] = config.get("database", "port")
DB_NAME: Final[str] = config.get("database", "database")
SERVER_PORT: Final[int] = config.getint("server", "port")
SERVER_BRIDGE_NET_ALIAS: Final[str] = config.get("server", "bridge_net_alias")

app = FastAPI()


@app.get("/")
async def get_data():
    with closing(psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
                                  host=DB_HOST_ALIAS, port=DB_PORT, database=DB_NAME)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT name, age from data;")
            data = [row for row in cursor]
            return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@app.get("/health")
async def hello_health():
    return JSONResponse(content=jsonable_encoder({"status": "OK"}), status_code=status.HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host=SERVER_BRIDGE_NET_ALIAS, port=SERVER_PORT)
