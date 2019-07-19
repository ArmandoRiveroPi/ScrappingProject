from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor, AdsDBWriter
from RevolicoProject.DataBase import DataBase
import time

start = time.time()

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
# rawData = RawDataProvider(baseFolder)

# scrapper = Scrapper(rawData)

# prep = Preprocessor()

# data = scrapper.scrap_data(10)
# prepdata = prep.preprocess_data(data)

db = DataBase()
db.create_users_table()
# writer = AdsDBWriter(db)

# writer.write_ads(prepdata)
user = {
    'user_id': '1',
    'phone_numbers': '78889933,78883567',
    'ad_set': '["12121212", "32323232"]'
}

db.write_user(user)

end = time.time()

print('Took ' + str(end - start) + ' seconds')
