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
data = scrapper.scrap_data(2)


prep = Preprocessor()
prepdata = prep.preprocess_data(data)

db = DataBase()
db.create_tables()


writer = AdsDBWriter(db)
writer.write_ads(prepdata)

usersB = UsersBuilder(db)
usersB.build_users()


end = time.time()

print('Took ' + str(end - start) + ' seconds')
