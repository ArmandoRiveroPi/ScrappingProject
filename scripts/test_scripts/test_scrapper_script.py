from RevolicoProject.DataPreparation import RawDataProvider, Scrapper
import time

start = time.time()

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
rawData = RawDataProvider(baseFolder)

scrapper = Scrapper(rawData)

data = scrapper.scrap_by_interval(100, 110)
print(data)

end = time.time()

print('Took ' + str(round(end - start, 2)) + ' seconds total')
