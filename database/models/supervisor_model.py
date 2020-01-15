from peewee import IntegerField, CharField
from database import connection


class Supervisor(connection.BaseModel):
    id = IntegerField(primary_key=True)
    description = CharField()

    class Meta:
        table_name = "supervisor"
