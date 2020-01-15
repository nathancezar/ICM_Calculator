from peewee import IntegerField, ForeignKeyField, DoubleField, BlobField, CharField, fn
from database import connection
from database.models.video_model import Video
from database.models.item_model import Item
from database.models.position_model import Position


class Result(connection.BaseModel):
    frame = IntegerField()
    image = CharField(null=True)
    information = IntegerField(null=True)
    item = ForeignKeyField(column_name='item_id', field='id', model=Item)
    km = IntegerField(null=True)
    video = ForeignKeyField(column_name='video_id', field='id', model=Video)
    position = ForeignKeyField(column_name='position_id', field='id', model=Position)

    class Meta:
        table_name = 'result'

def getByVideo(video):
    try:
        return Result.select().where(Result.video == video.id)
    except Result.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def getTotalsByVideo(video):
    try:
        return (Result
                .select(Result.item, fn.COUNT(Result.id).alias('total'))
                .where(Result.video == video.id)
                .group_by(Result.item))
    except Result.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
