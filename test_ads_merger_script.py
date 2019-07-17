from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor, AdsDBWriter
from RevolicoProject.DataBase import DataBase
import time

start = time.time()

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
rawData = RawDataProvider(baseFolder)

scrapper = Scrapper(rawData)

prep = Preprocessor()

data = scrapper.scrap_data(1000)
prepdata = prep.preprocess_data(data)

db = DataBase()
# db.create_ads_table()
writer = AdsDBWriter(db)

writer.write_ads(prepdata)

# ad = db.read_ad('30307274')
# ad = db.find_ads_by_field(
#     'title', 'Asus VivoBook | 15.6 FHD | i5-8va | 8GB RAM | 128SSD+1TB | Lector Huella | 0Km')
# print(ad)
# ads = db.find_ads_by_title('Mariachi')
# for ad in ads:
#     print(ad)


end = time.time()

print('Took ' + str(end - start) + ' seconds')
