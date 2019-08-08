"""This module is concerned with creating the webserver database
from the model training data.

Because of that, it depends both in knowing and probably connecting
with both databases.
It should provide a web server database ready for the server to use.
"""
from .data_base_class import DataBase
from sqlalchemy import MetaData, Table, Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

# You have to make all the db operations under this same base,
# otherwise the ORM might not work properly
DeclarativeBase = declarative_base()


class WebAdvert(DeclarativeBase):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'revolico_ads'

    ad_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    # price = Column(String)
    # classification = Column(String)
    # # relationship("SQLAlchemyUser", back_populates='adverts')
    # user = Column(Integer, ForeignKey('users.user_id'))
    phone = Column(String)  # Coma separated list of phone numbers
    # datetime = Column(DateTime)


class WebBperson(DeclarativeBase):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'revolico_bperson'

    bperson_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    # name_set = Column(Text)
    # adverts = relationship("SQLAlchemyAdvert")
    # ads_amount = Column(Integer)


class WebDataBase:
    """Main class to encapsulate the DB functionality

    Right now mostly relying on SQL Alchemy
    """

    def __init__(self, dbName='revolico_web'):
        self.user = 'postgres'
        self.dbName = dbName
        self.password = 'root'
        self.host = 'localhost:5432'
        self.dbString = "postgres://{user}:{password}@{host}/{db}".format(
            user=self.user, password=self.password, host=self.host, db=self.dbName)
        self.cursor = create_engine(self.dbString)
        self.session = sessionmaker(self.cursor)()
        self.adType = WebAdvert()
        self.userType = WebBperson()


class WebDataBaseMigrator(object):

    def __init__(self, trainDB: DataBase, webDB: WebDataBase):
        self.trainDB = trainDB
        self.webDB = webDB

    def migrate_ads(self, amount=10):
        ads = self.trainDB.get_all_ads()
        counter = 0
        for ad in ads:
            if amount > 0 and counter >= amount:
                break
            counter += 1
            self.migrate_ad(ad.ad_id)

    def migrate_ad(self, adID):
        """Read an ad from the Train DB and copy it to the Web DB
        """
        trainAd = self.trainDB.get_ad_by_id(adID)
        # Try to get the element by ID
        oldAd = self.webDB.session.query(WebAdvert).get(adID)
        # If the element exists only modify it
        if oldAd:
            oldAd.title = trainAd.title
            oldAd.content = trainAd.content
            oldAd.phone = trainAd.user_phone
        else:
            # If the element doesn't exist, you need to add it
            newAd = WebAdvert()
            newAd.ad_id = adID
            newAd.title = trainAd.title
            newAd.content = trainAd.content
            newAd.phone = trainAd.user_phone
            self.webDB.session.add(newAd)
        self.webDB.session.commit()
