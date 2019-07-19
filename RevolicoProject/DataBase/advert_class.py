"""This module holds the class to encapsulate an advert and to centralize
all advert representations.

Includes:
advert fields to scrap by the scrapper
advert class for sqlalchemy
"""

from sqlalchemy import MetaData, Table, Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
# from .revo_user_class import SQLAlchemyUser

base = declarative_base()


class Advert:
    fields = {
        "ad_id": {
            "scrapCode": 'find(text=re.compile(".*Id:")).parent.nextSibling.nextSibling.get_text()',
            'default': '11111111',
        },
        "title": {
            "scrapCode": 'h1.get_text()',
            'default': '',
        },
        "content": {
            "scrapCode": 'find("span", class_="showAdText").get_text()',
            'default': '',
        },
        "datetime": {
            "scrapCode": 'find(text=re.compile(".*Fecha:")).parent.nextSibling.nextSibling.get_text()',
            'default': '-infinity',
        },
        "price": {
            "scrapCode":  'find(text=re.compile(".*Precio:")).parent.nextSibling.nextSibling.get_text()',
            'default': '',
        },
        "user": {  # relationship
            'default': "",
        },
        "user_name": {
            "scrapCode": 'find(text=re.compile(".*Nombre:")).parent.nextSibling.nextSibling.get_text()',
            'default': '',
        },
        "user_phone": {
            "scrapCode": 'find(text=re.compile(".*fono:")).parent.nextSibling.nextSibling.get_text()',
            'default': '',
        },
        "classification": {
            "scrapCode": 'find(id="pathaway").get_text()',
            'default': '',
        },
        "is_renewable": {
            "scrapCode": 'find(id="auto_renew_hint")',
            'default': False,
        },
        "extra_data": {
            'default': "{}",
        },

    }

# ------  SUPPORT CLASSES FOR DB OBJECTS -----------


class SQLAlchemyAdvert(base):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'ads'

    ad_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    price = Column(String)
    classification = Column(String)  # coma separated list of classifications
    # relationship("SQLAlchemyUser", back_populates='adverts')
    user = Column(Integer, ForeignKey('users.user_id'))
    user_name = Column(String)
    user_phone = Column(String)  # Coma separated list of phone numbers
    datetime = Column(DateTime)
    is_renewable = Column(Boolean)
    extra_data = Column(Text)  # Free format JSON data associated with the Ad


class AdsTable:
    def __init__(self, dbString):
        self.db = create_engine(dbString)
        self.meta = MetaData(self.db)
        self.table = Table('ads', self.meta,
                           Column('ad_id', Integer, primary_key=True),
                           Column('title', String),
                           Column('content', Text),
                           Column('price', String),
                           # coma separated list of classifications
                           Column('classification', String),
                           #    Column('user', relationship(
                           #        "SQLAlchemyUser", back_populates='adverts')),
                           Column('user', Integer, ForeignKey('users.user_id')),
                           Column('user_name', String),
                           # Coma separated list of phone numbers
                           Column('user_phone', String),
                           Column('datetime', DateTime),
                           Column('is_renewable', Boolean),
                           # Free format JSON data associated with the Ad
                           Column('extra_data', Text),
                           )
