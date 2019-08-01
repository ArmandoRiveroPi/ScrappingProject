from sqlalchemy import Column, Integer, BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base

EtecsaBase = declarative_base()


class SQLAlchemyMobile(EtecsaBase):
    """Class to represent an mobile phone to the SQLAlchemy ORM

    """
    __tablename__ = 'mobile'

    number = Column(BigInteger, primary_key=True)
    name = Column(String)
    identification = Column(String)
    address = Column(Text)
    province = Column(Integer)


class SQLAlchemyLandline(EtecsaBase):
    """Class to represent an landline phone to the SQLAlchemy ORM

    """
    __tablename__ = 'landline'

    number = Column(BigInteger, primary_key=True)
    name = Column(String)
    identification = Column(String)
    address = Column(Text)
    province = Column(Integer)


class Phone(object):
    """Represents a phone entity
    """

    fields = {
        "number": {
            'default': '00000000',
        },
        "name": {
            'default': '',
        },
        "identification": {
            'default': '',
        },
        "address": {
            'default': '',
        },
        "province": {
            'default': 0,
        },
    }

    def from_obj_to_dic(self, obj):
        phoneDic = {}
        for field, fieldInfo in self.fields.items():
            phoneDic[field] = getattr(obj, field, fieldInfo['default'])
        return phoneDic

    def from_dic_to_obj(self, phoneDic, phoneClass):
        phoneObj = phoneClass()
        for field in phoneDic:
            setattr(phoneObj, field, phoneDic[field])
        return phoneObj
