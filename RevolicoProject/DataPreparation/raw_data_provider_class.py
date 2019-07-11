import re
import os


class RawDataProvider(object):
    """Provides access to the raw data in an organized way

    The raw data could be in files or in urls or in a DB, etc.
    So this class abstracts these variations away, providing raw strings of
    data that later need to be parsed or scrapped for valuable data.

    Depends of how are the data files stored (what names, if in disc or in the web, etc)
    Provides access to the files content
    """

    def __init__(self, baseFolder):
        """constructor of RawDataClass

        Arguments:
            baseFolder {string} -- absolute path of the folder where the data is
        """
        self.folder = baseFolder
        self.goodRE = re.compile('.*(\d{8,})\.html')
        self.fileNames = []
        self.fileAccessors = []

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
        return self.fileNames

    def get_file_accessors(self):
        self.get_file_names()
        for filename in self.fileNames:
            self.fileAccessors.append(FileAccessor(filename))
        return self.fileAccessors

    def test_file_access(self):
        """Some simple human tests to check everything is working with the class
        """
        self.get_file_accessors()
        print("Total Files ", len(self.fileNames))
        print(self.fileAccessors[-1].get_base_path())


class FileAccessor:
    def __init__(self, fileURI=''):
        self.fileURI = fileURI

    def get_content(self, encoding="utf-8"):
        with open(self.fileURI, mode='r', encoding=encoding, errors="ignore") as f:
            content = f.read()
        return content

    def get_filename(self):
        return os.path.basename(self.fileURI)

    def get_base_path(self):
        return os.path.dirname(self.fileURI)
