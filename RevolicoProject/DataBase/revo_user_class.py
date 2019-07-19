"""This modules handles the data structure definition for the User type
Specially important is the database schema
"""

from sqlalchemy import MetaData, Table, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from .advert_class import SQLAlchemyAdvert

base = declarative_base()


class RevoUser:
    fields = {
        "user_id": {
            'default': '1',
        },
        "name": {
            'default': '',
        },

        "phone_numbers": {
            'default': '',
        },

        "name_set": {
            'default': '',
        },

        "adverts": {
            'default': '',
        },

    }

    def from_obj_to_dic(self, obj):
        userDic = {}
        for field, fieldInfo in self.fields.items():
            userDic[field] = getattr(obj, field, fieldInfo['default'])

    def from_dic_to_obj(self, userDic):
        userObj = SQLAlchemyUser()
        for field in userDic:
            setattr(userObj, field, userDic[field])

# ------  SUPPORT CLASSES FOR DB OBJECTS -----------


class SQLAlchemyUser(base):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_numbers = Column(String)
    name_set = Column(Text)
    # , order_by=SQLAlchemyAdvert.ad_id,back_populates="user"
    adverts = relationship("SQLAlchemyAdvert")


class UsersTable:
    def __init__(self, dbString):
        self.db = create_engine(dbString)
        self.meta = MetaData(self.db)
        self.table = Table('users', self.meta,
                           Column('user_id', Integer, primary_key=True),
                           # list of phone numbers
                           Column('name', String),
                           Column('phone_numbers', String),
                           # list of ads ids linked to user
                           Column('name_set', Text),
                           #    Column('adverts', relationship("SQLAlchemyAdvert")),
                           )
