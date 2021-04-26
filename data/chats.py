import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Chats(SqlAlchemyBase, UserMixin):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    first_user_id = sqlalchemy.Column(sqlalchemy.Integer)
    second_user_id = sqlalchemy.Column(sqlalchemy.Integer)
    # messages = orm.relation("Messages", back_populates='chatId', view)
