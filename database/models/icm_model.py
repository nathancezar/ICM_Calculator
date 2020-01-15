__author__ = 'Equipe-ECV'

from peewee import IntegerField, ForeignKeyField, DoubleField, BooleanField, SQL
from database import connection
from database.models.highway_model import Highway

class Icm(connection.BaseModel):
    highway = ForeignKeyField(column_name="highway_id", field='id', model=Highway)
    km = IntegerField(null=True)
    direction = IntegerField(null=True)
    pothole = IntegerField(null=True)
    repair = IntegerField(null=True)
    crack = DoubleField(null=True)
    clearing = DoubleField(null=True)
    signal = IntegerField(null=True)
    drainage = IntegerField(null = True)
    icp = DoubleField(null=True)
    icc = DoubleField(null=True)
    icm = DoubleField(null=True)
    sent = BooleanField(constraints=[SQL("DEFAULT FALSE")])

    class Meta:
        table_name = "icm"

def getIcmByHighway(highway):
    try:
        return Icm.select().where(Icm.highway == highway).get()
    except Icm.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getIcmByKm(highway, km):
    try:
        return Icm.select().where(Icm.highway == highway and
                                  Icm.km == km).get()
    except Icm.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
