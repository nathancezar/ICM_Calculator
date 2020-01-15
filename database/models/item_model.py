from peewee import CharField
from database import connection


class Item(connection.BaseModel):
    description = CharField(max_length=10)

    class Meta:
        table_name = 'item'
