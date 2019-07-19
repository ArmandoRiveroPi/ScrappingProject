import time
from RevolicoProject.DataBase import DataBase
from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor, AdsDBWriter, UsersBuilder

from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


start = time.time()

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
rawData = RawDataProvider(baseFolder)

scrapper = Scrapper(rawData)

prep = Preprocessor()

data = scrapper.scrap_data(10)
prepdata = prep.preprocess_data(data)

db = DataBase()
db.create_tables()

# user = 'postgres'
# dbName = 'revolico'
# password = 'root'
# host = 'localhost:5432'
# dbString = "postgres://{user}:{password}@{host}/{db}".format(
#     user=user, password=password, host=host, db=dbName)
# cursor = create_engine(dbString)
# session = sessionmaker(cursor)()
# Base = declarative_base()


# class SQLAlchemyUser(Base):
#     """Class to represent an advert to the SQLAlchemy ORM

#     Arguments:
#         base {object} -- declarative_base() built object to inherit from
#     """
#     __tablename__ = 'users'

#     user_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     phone_numbers = Column(String)
#     name_set = Column(Text)
#     # , order_by=SQLAlchemyAdvert.ad_id,back_populates="user"
#     adverts = relationship("SQLAlchemyAdvert")


# class SQLAlchemyAdvert(Base):
#     """Class to represent an advert to the SQLAlchemy ORM

#     Arguments:
#         base {object} -- declarative_base() built object to inherit from
#     """
#     __tablename__ = 'ads'

#     ad_id = Column(Integer, primary_key=True)
#     title = Column(String)
#     content = Column(Text)
#     price = Column(String)
#     classification = Column(String)  # coma separated list of classifications
#     # relationship("SQLAlchemyUser", back_populates='adverts')
#     user = Column(Integer, ForeignKey('users.user_id'))
#     user_name = Column(String)
#     user_phone = Column(String)  # Coma separated list of phone numbers
#     datetime = Column(DateTime)
#     is_renewable = Column(Boolean)
#     extra_data = Column(Text)  # Free format JSON data associated with the Ad


# Base.metadata.create_all(cursor)

writer = AdsDBWriter(db)
writer.write_ads(prepdata)

usersB = UsersBuilder(db)
usersB.build_users()

# user = {
#     'user_id': '1',
#     'phone_numbers': '78889933,78883567',
#     'ad_set': '["12121212", "32323232"]'
# }

# db.write_user(user)


end = time.time()

print('Took ' + str(end - start) + ' seconds')
