import os

from peewee import *
from dotenv import load_dotenv

load_dotenv()

pg_db = PostgresqlDatabase(os.environ.get("BOT_DB_NAME"),
                           user=os.environ.get("BOT_DB_USER"),
                           password=os.environ.get("BOT_DB_PASS"),
                           host=os.environ.get("BOT_DB_HOST"),
                           port=os.environ.get("BOT_DB_PORT"))


class BaseModel(Model):
    class Meta:
        database = pg_db


class User(BaseModel):
    id = PrimaryKeyField()
    name = TextField()