from sqlalchemy import MetaData, Table, Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

# You have to make all the db operations under this same base,
# otherwise the ORM might not work properly
DeclarativeBase = declarative_base()


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
            'default': None,
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


class SQLAlchemyAdvert(DeclarativeBase):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'ads'

    ad_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    price = Column(String)
    # coma separated list of classifications
    classification = Column(String)
    # relationship("SQLAlchemyUser", back_populates='adverts')
    user = Column(Integer, ForeignKey('users.user_id'))
    user_name = Column(String)
    user_phone = Column(String)  # Coma separated list of phone numbers
    datetime = Column(DateTime)
    is_renewable = Column(Boolean)
    # Free format JSON data associated with the Ad
    extra_data = Column(Text)


# class AdsTable:
#     def __init__(self, dbString):
#         self.db = create_engine(dbString)
#         self.meta = MetaData(self.db)
#         self.table = Table('ads', self.meta,
#                            Column('ad_id', Integer, primary_key=True),
#                            Column('title', String),
#                            Column('content', Text),
#                            Column('price', String),
#                            # coma separated list of classifications
#                            Column('classification', String),
#                            #    Column('user', relationship(
#                            #        "SQLAlchemyUser", back_populates='adverts')),
#                            Column('user', Integer, ForeignKey('users.user_id')),
#                            Column('user_name', String),
#                            # Coma separated list of phone numbers
#                            Column('user_phone', String),
#                            Column('datetime', DateTime),
#                            Column('is_renewable', Boolean),
#                            # Free format JSON data associated with the Ad
#                            Column('extra_data', Text),
#                            )


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
        userObj = sqlalchemy_object_factory('user', )
        for field in userDic:
            setattr(userObj, field, userDic[field])


class SQLAlchemyUser(DeclarativeBase):
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


# class UsersTable:
#     def __init__(self, dbString):
#         self.db = create_engine(dbString)
#         self.meta = MetaData(self.db)
#         self.table = Table('users', self.meta,
#                            Column('user_id', Integer, primary_key=True),
#                            # list of phone numbers
#                            Column('name', String),
#                            Column('phone_numbers', String),
#                            # list of ads ids linked to user
#                            Column('name_set', Text),
#                            #    Column('adverts', relationship("SQLAlchemyAdvert")),
#                            )
