from peewee import CharField, ForeignKeyField, DateField
from database import connection
from database.models.supervisor_model import Supervisor


class Contract(connection.BaseModel):
    code = CharField(max_length=10, null=True)
    final_date = DateField()
    initial_date = DateField()
    state = CharField(max_length=2, null=True)
    supervisor = ForeignKeyField(column_name='supervisor_id', field='id', model=Supervisor)

    class Meta:
        table_name = 'contract'

def getContractById(id):
    try:
        return Contract.select().where(Contract.id == id).get()
    except Contract.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
