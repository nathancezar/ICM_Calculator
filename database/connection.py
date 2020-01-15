import os
from peewee import SqliteDatabase, Model

dirpath = os.path.abspath(os.path.dirname(__file__))
path = lambda string: os.path.join(dirpath, string)

database = SqliteDatabase(path("/home/daniel/Documents/935/database/icm.db"), pragmas={
    'foreign_keys': 1,
})


class BaseModel(Model):
    class Meta:
        database = database