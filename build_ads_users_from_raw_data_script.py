import time
from RevolicoProject.DataBase import DataBase
from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor, AdsDBWriter, UsersBuilder

start = time.time()

# Complete data folder
# baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
# small testing folder
baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/min_data_folder"
rawData = RawDataProvider(baseFolder)

rawData.get_file_names()
fileAmount = rawData.fileAmount

# Initializations
scrapper = Scrapper(rawData)
prep = Preprocessor()
db = DataBase()
db.create_tables()
writer = AdsDBWriter(db)
usersB = UsersBuilder(db)

# Process data by chunks
chunkSize = 100
totalChunks = int(fileAmount/chunkSize) + 1
for chunk in range(totalChunks):
    startChunk = chunk * chunkSize
    endChunk = (chunk + 1) * chunkSize
    print('Starting chunk ' + str(chunk + 1) + '/' + str(totalChunks) + ' ---> from ' +
          str(startChunk) + ' to ' + str(endChunk) + ' out of ' + str(fileAmount))
    data = scrapper.scrap_by_interval(startChunk, endChunk)
    prepdata = prep.preprocess_data(data)
    writer.write_ads(prepdata)
    usersB.build_users()
    print('---> Chunk ' + str(chunk) + ' at ' +
          str(time.time() - start) + ' seconds')


end = time.time()

print('Took ' + str(end - start) + ' seconds total')
