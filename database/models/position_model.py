from peewee import ForeignKeyField, DoubleField, CharField
from database import connection
from database.models.video_model import Video


class Position(connection.BaseModel):
    latitude = DoubleField(null=True)  # double precision
    longitude = DoubleField(null=True)  # double precision
    distance = DoubleField(null=True)  # double precision
    snv_code = CharField(max_length=10, null=True)
    video = ForeignKeyField(column_name='video_id', field='id', model=Video)

    class Meta:
        table_name = 'position'

def getByVideo(video):
    try:
        return (Position
                .select()
                .where(Position.video == video.id)
                .order_by(Position.id))
    except Position.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
