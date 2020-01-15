from peewee import Model, CharField, ForeignKeyField, DoubleField
from database import connection
from database.models.contract_model import Contract

class Highway(connection.BaseModel):
    contract = ForeignKeyField(column_name='contract_id', field='id', model=Contract)
    highway = CharField(max_length=3, null=True)
    km_f = DoubleField(null=True)
    km_i = DoubleField(null=True)

    class Meta:
        table_name = 'highway'

def getHighwayById(id):
    try:
        return Highway.select().where(Highway.id == id).get()
    except Highway.DoesNotExist:
        return None
    except Exception as ex:
        raise ex