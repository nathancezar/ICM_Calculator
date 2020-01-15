__author__ = 'Equipe-ECV'

from peewee import IntegerField, BooleanField, DateTimeField, ForeignKeyField, SQL, fn
from database import connection
from database.models.result_model import Result
from database.models.position_model import Position
from database.models.video_model import Video


class PosProcessingResult(connection.BaseModel):
    condition = IntegerField(null=True)
    pos_processed = BooleanField(constraints=[SQL("DEFAULT FALSE")])
    pos_processing_date = DateTimeField(null=True)
    positive = BooleanField(constraints=[SQL("DEFAULT FALSE")])
    result = ForeignKeyField(column_name='result_id', field='id', model=Result)

    class Meta:
        table_name = 'pos_processing_result'

def getResultsByHighway(highway, direction):
    """
        Return a dictionary with the post processed results of the highway and 
        direction past
    """
    try:
        return (Result
                .select(Result.item, fn.COUNT(Result.id).alias("total"), fn.ROUND(Position.distance/1000).alias('Km_Calc'))
                .join(Position)
                .join(PosProcessingResult, on=(PosProcessingResult.result == Result.id))
                .join(Video, on=(Video.id == Result.video))
                .where(PosProcessingResult.positive == True)
                .where(PosProcessingResult.pos_processed == True)
                .where(Video.highway == highway)
                .where(Video.direction == direction)
                .where(Result.item != 6)
                .where(Result.item != 7)
                .group_by(SQL('Km_Calc'), Result.item)
        )
    except Result.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
