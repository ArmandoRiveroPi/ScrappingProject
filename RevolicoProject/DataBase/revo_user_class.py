"""This modules handles the data structure definition for the User type
Specially important is the database schema
"""

from sqlalchemy import MetaData, Table, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

base = declarative_base()


class RevoUser:
    fields = {
        "user_id": {
            'default': '1',
        },
        "phone_numbers": {
            'default': '',
        },
        "ad_set": {
            'default': '',
        },

    }

# ------  SUPPORT CLASSES FOR DB OBJECTS -----------


class SQLAlchemyUser(base):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    phone_numbers = Column(String)
    ad_set = Column(Text)


class UsersTable:
    def __init__(self, dbString):
        self.db = create_engine(dbString)
        self.meta = MetaData(self.db)
        self.table = Table('users', self.meta,
                           Column('user_id', Integer, primary_key=True),
                           # list of phone numbers
                           Column('phone_numbers', String),
                           # list of ads ids linked to user
                           Column('ad_set', Text),
                           )
