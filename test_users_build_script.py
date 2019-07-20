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

data = scrapper.scrap_data(5)
prepdata = prep.preprocess_data(data)

db = DataBase()
db.create_tables()


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
