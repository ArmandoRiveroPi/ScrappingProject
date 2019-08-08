from RevolicoProject.AppFunctionality import ProductExtractor
from RevolicoProject.DataBase import DataBase
import time
import pandas as pd

start = time.time()

dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump.csv'

df = pd.read_csv(dataFile)  # [0:10000]
print('Amount of data', df.shape[0])
df = df.sample(n=10).reset_index(drop=True)

# db = DataBase()
extractor = ProductExtractor()

# ids = ['30658574', '28109689', '29188696', '30398521', '29546416']

for adDic in df.to_dict(orient='records'):
    # ad = db.get_ad_by_id(adID)
    # adDic = db.advert_to_dic(ad)
    product = extractor.extract_product(adDic)
    print('='*20, '>>', product)


# def extract(adID):
#     ad = db.get_ad_by_id(adID)
#     adDic = db.advert_to_dic(ad)
#     product = extractor.extract_product(adDic)
#     print('='*20, '>>', product)


end = time.time()
print('Took', end - start, 'seconds')
