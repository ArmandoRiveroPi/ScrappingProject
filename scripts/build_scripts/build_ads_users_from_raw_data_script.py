import time
from RevolicoProject.DataBase import DataBase
from RevolicoProject.DataPreparation import RawDataProvider, Scrapper, Preprocessor, AdsDBWriter, UsersBuilder
from multiprocessing import Pool
import math

start = time.time()


def build_subchunk(args):
    """This is for parallelization purposes

    Arguments:
        args {[type]} -- [description]
    """
    baseFolder = args[2]
    rawData = RawDataProvider(baseFolder)
    rawData.get_file_names()
    scrapper = Scrapper(rawData)
    prep = Preprocessor()
    db = DataBase()
    db.create_tables()
    writer = AdsDBWriter(db)

    data = scrapper.scrap_by_interval(args[0], args[1])
    prepdata = prep.preprocess_data(data)
    writer.write_ads(prepdata)


# end, scrapper, preprocessor, writer
def subchunk_args_array(cores, start, end, baseFolder):
    """This is for parallelization purposes

    Arguments:
        cores {[type]} -- [description]
        start {[type]} -- [description]
        end {[type]} -- [description]
        baseFolder {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    total = end - start
    subchunkSize = math.ceil(total/cores)
    argsArray = [
        (start + core * subchunkSize, start +
         (core + 1) * subchunkSize, baseFolder)
        for core in range(cores)
    ]
    return argsArray


def percent(part, total):
    return round((part/total)*100, 2)


# Complete data folder
baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [16-07-19]"
# small testing folder
# baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/min_data_folder"

# Initializations
rawData = RawDataProvider(baseFolder)
rawData.get_file_names()
fileAmount = rawData.fileAmount
# scrapper = Scrapper(rawData)
# prep = Preprocessor()
db = DataBase()
db.create_tables()
# writer = AdsDBWriter(db)
usersB = UsersBuilder(db)


# Process data by chunks and in parallel
cores = 2
subChunkSize = 200
chunkSize = cores * subChunkSize
totalChunks = int(fileAmount / chunkSize) + 1
firstChunk = 0
with Pool(processes=cores) as pool:
    print('Chunks', totalChunks)
    for chunk in range(firstChunk, totalChunks):
        startTime = time.time()
        startChunk = chunk * chunkSize
        endChunk = (chunk + 1) * chunkSize
        print('Starting chunk', chunk + 1, '/', totalChunks, '[', percent(chunk+1, totalChunks),
              '%] ---> from', startChunk, 'to', endChunk, 'out of', fileAmount)
        args = subchunk_args_array(cores, startChunk, endChunk, baseFolder)
        pool.map(build_subchunk, args)
        endTime = time.time()
        print('>'*50, 'Finished chunk', chunk + 1, '/', totalChunks,
              '[', percent(chunk+1, totalChunks), '%]  in', round(endTime - startTime), 'seconds')


usersB.build_users()
end = time.time()

print('Took ' + str(round(end - start)) + ' seconds total')
