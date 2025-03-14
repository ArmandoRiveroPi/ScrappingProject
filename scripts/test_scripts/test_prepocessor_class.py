from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor
import time

start = time.time()

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
rawData = RawDataProvider(baseFolder)

scrapper = Scrapper(rawData)

prep = Preprocessor()

data = scrapper.scrap_data(20)
prepdata = prep.preprocess_data(data)
for dic in prepdata:
    print('ID--> ' + dic['ad_id'] + ' Phone --> ' + dic['user_phone'])
    # print('Classification: ' +
    #       dic['classification'] + ' *** Price: ' + dic['price'])
    # print(dic['classification'])


end = time.time()

print('Took ' + str(end - start) + ' seconds')
