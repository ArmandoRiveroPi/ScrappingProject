from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()


class DataBase:
    """Main class to encapsulate the DB functionality
    """

    def __init__(self):
        self.user = 'postgres'
        self.dbName = 'revolico'
        self.password = 'root'
        self.host = 'localhost:5432'
        dbString = "postgres://{user}:{password}@{host}/{db}".format(
            user=self.user, password=self.password, host=self.host, db=self.dbName)
        self.cursor = create_engine(dbString)
        self.session = sessionmaker(self.cursor)()

    def create_ads_table(self):
        base.metadata.create_all(self.cursor)
        exampleAd = SQLAlchemyAdvert(
            adID=1,
            title='kk',
            content='kk',
            classification='kk',
            user_name='kk',
            user_phone='53174025',
            datetime='now',
            is_renewable=True
        )
        self.session.add(exampleAd)
        self.session.commit()


# ------  SUPPORT CLASSES FOR DB OBJECTS -----------

class SQLAlchemyAdvert(base):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'ads'

    adID = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    classification = Column(String)
    user_name = Column(String)
    user_phone = Column(String)
    datetime = Column(DateTime)
    is_renewable = Column(Boolean)


# class SQLAlchemyUser(object):
#     pass
