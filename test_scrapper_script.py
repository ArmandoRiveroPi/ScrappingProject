from RevolicoProject.DataPreparation import RawDataProvider, Scrapper

baseFolder = "/home/gauss/arm/importante/work/ai/projects/revolico/Revolico [A FULL CON BUSCADOR] [25-06-19]"
rawData = RawDataProvider(baseFolder)

scrapper = Scrapper(rawData)

scrapper.test_scrapper()
