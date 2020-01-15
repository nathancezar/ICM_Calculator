from peewee import IntegerField, CharField, ForeignKeyField, DoubleField, DateField, DateTimeField, BooleanField, TextField, SQL
from database import connection
from database.models.highway_model import Highway

class Video(connection.BaseModel):
    clearing_total = IntegerField(null=True)
    crack_total = IntegerField(null=True)
    direction = IntegerField(null=True)
    drainage_total = IntegerField(null=True)
    hash = TextField()
    highway = ForeignKeyField(column_name='highway_id', field='id', model=Highway)
    km_f = DoubleField(null=True)
    km_i = DoubleField(null=True)
    name = CharField(max_length=20, null=True)
    pos_processes = BooleanField(constraints=[SQL("DEFAULT FALSE")])
    pothole_total = IntegerField(null=True)
    processing_date = DateTimeField(constraints=[SQL("DEFAULT datetime('now')")])
    repair_total = IntegerField(null=True)
    signal_total = IntegerField(null=True)
    recording_date = DateField(null=True)

    class Meta:
        table_name = 'video'

def getVideoByHash(hash):
    try:
        return Video.select().where(Video.hash == hash).get()
    except Video.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
