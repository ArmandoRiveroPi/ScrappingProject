from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor, AdsDBWriter
from RevolicoProject.DataBase import DataBase
import time

start = time.time()

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
rawData = RawDataProvider(baseFolder)

scrapper = Scrapper(rawData)

prep = Preprocessor()

data = scrapper.scrap_data(10)
prepdata = prep.preprocess_data(data)

db = DataBase()
db.create_users_table()
# writer = AdsDBWriter(db)

# writer.write_ads(prepdata)


end = time.time()

print('Took ' + str(end - start) + ' seconds')
