import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Messages(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    chatId = sqlalchemy.Column(sqlalchemy.Integer)
    authorId = sqlalchemy.Column(sqlalchemy.Integer)
    content = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
