import re
import os


class RawDataProvider(object):
    """Provides access to the raw data in an organized way

    The raw data could be in files or in urls or in a DB, etc.
    So this class abstracts these variations away, providing raw strings of
    data that later need to be parsed or scrapped for valuable data.
    """

    def __init__(self, baseFolder):
        """constructor of RawDataClass

        Arguments:
            baseFolder {string} -- absolute path of the folder where the data is
        """
        self.folder = baseFolder
        self.goodRE = re.compile('.*(\d{8,})\.html')
        self.fileNames = []

    def is_good_file(self, filename):
        """Tests wether the file name is well formed

        Arguments:
            filename {string} -- name of the file to be tested

        Returns:
            [bool] -- whether the filename if well formed
        """
        return self.goodRE.match(filename)

    def get_file_names(self):
        """Builds the list of good data files
        """
        for root, dirs, files in os.walk(self.folder):
            cleanFiles = [os.path.join(root, file)
                          for file in files if self.is_good_file(file)]
            self.fileNames += cleanFiles
            # print(cleanFiles)

    def test_file_access(self):
        """Some simple human tests to check everything is working with the class
        """
        self.get_file_names()
        print("Total Files ", len(self.fileNames))
        print(self.fileNames[0])
