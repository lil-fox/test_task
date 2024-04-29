import os

from peewee import *
from dotenv import load_dotenv

load_dotenv()

pg_db = PostgresqlDatabase(os.environ.get("DB_NAME"),
                           user=os.environ.get("DB_USER"),
                           password=os.environ.get("DB_PASS"),
                           host=os.environ.get("DB_HOST"),
                           port=os.environ.get("DB_PORT"))


class BaseModel(Model):
    class Meta:
        database = pg_db


class BotUsers(BaseModel):
    id = PrimaryKeyField()
    name = TextField()