import re
import os
import random


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
        self.goodRE = re.compile(r'.*(\d{8,})\.html$')
        self.fileNames = []
        self.fileAccessors = []
        self.fileAmount = 0

    def is_good_file(self, filename):
        """Tests wether the file name is well formed

        Arguments:
            filename {string} -- name of the file to be tested

        Returns:
            [bool] -- whether the filename if well formed
        """
        return self.goodRE.match(filename)

    def get_file_names(self, amount=0):
        """Builds the list of good data files
        """
        for root, dirs, files in os.walk(self.folder):
            cleanFiles = [os.path.join(root, file)
                          for file in files if self.is_good_file(file)]
            self.fileNames += cleanFiles
        # Now you know how many files do you have in total
        self.fileAmount = len(self.fileNames)
        amount = min(amount, self.fileAmount)
        if amount != 0:
            # pick an amount of random files
            # self.fileNames = random.sample(self.fileNames, amount)
            # pick the first amount of files
            self.fileNames = self.fileNames[0:amount]
        return self.fileNames

    def get_file_accessors(self, amount=0, buildFiles=True):
        # Clean the file accessors
        self.fileAccessors = []
        # Only build the file list if commanded
        if buildFiles:
            self.get_file_names(amount)
        # When amount == 0 means infinity, so behavior changes
        if amount > 0:
            for index in range(amount):
                self.fileAccessors.append(FileAccessor(self.fileNames[index]))
        else:
            for fileName in self.fileNames:
                self.fileAccessors.append(FileAccessor(fileName))

        return self.fileAccessors

    def get_accessors_slice(self, start=0, end=0):
        files = self.get_file_names(0)
        start = min(start, self.fileAmount)
        end = min(end, self.fileAmount)
        self.fileNames = files[start:end]
        self.get_file_accessors(0, False)
        return self.fileAccessors


class FileAccessor:
    def __init__(self, fileURI=''):
        self.fileURI = fileURI

    def get_content(self, encoding="ISO-8859-1"):
        with open(self.fileURI, mode='r', encoding=encoding, errors="replace") as f:
            content = f.read()
        return content

    def get_filename(self):
        return os.path.basename(self.fileURI)

    def get_base_path(self):
        return os.path.dirname(self.fileURI)
