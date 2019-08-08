from RevolicoProject.DataBase import WebDataBaseMigrator, WebDataBase, DataBase


webDB = WebDataBase()
trainDB = DataBase()
migrator = WebDataBaseMigrator(trainDB, webDB)

migrator.migrate_ads(20)
