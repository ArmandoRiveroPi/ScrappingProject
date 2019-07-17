import re
import sys
from bs4 import BeautifulSoup
from multiprocessing import Pool
from ..DataBase import Advert


class Scrapper:
    """Encapsulates the scrapping functionality

    The scrapper only cares of extracting the desired data from HTML or other formated strings
    Should work with a raw data provider that gives the scrapper these strings to scrap from.

    Depends on the location of data inside the html content
    Provides data fields of the html files
    """

    def __init__(self, RawDataProvider):
        self.provider = RawDataProvider
        self.accessors = []
        self.adType = Advert()

    def build_accessors(self, amount=0):
        self.accessors = self.provider.get_file_accessors(amount)
        return self.accessors

    # def build_bs_object(self, accessor):
    #     return BeautifulSoup(accessor.get_content(), features="html5lib")

    def get_field(self, bsCode='',  amount=0, bsObjects=[]):
        """Extracts data from a field by a Beautiful Soup code

        Keyword Arguments:
            bsCode {str} -- the Beautiful Soup code to be executed over the html (default: {''})
            amount {int} -- amount of elements to be scrapped (default: {0})
            bsObjects {list} -- a list of cached Beautiful Soup objects to prevent building them again (default: {[]})

        Returns:
            [list] -- list of values scrapped
        """
        fieldData = []
        if amount == 0:
            amount = len(self.accessors)
        for index in range(amount):
            if len(bsObjects) > index:
                soup = bsObjects[index]
            else:
                soup = BeautifulSoup(
                    self.accessors[index].get_content(), features="html5lib")
            try:
                fieldData.append(str(eval('soup.' + bsCode)))
            except AttributeError:
                fieldData.append('')
        return fieldData

    def scrap_data(self, amount=0):
        """Scraps some amount of files for all the fields

        Keyword Arguments:
            amount {int} -- how many files to scrap (default: {0})

        Returns:
            [list] -- list of dictionaries with the fields scrapped and their values
        """
        # Build accessors
        self.build_accessors(amount)
        # Build bs objects
        bsObjects = [BeautifulSoup(self.accessors[i].get_content(), features="html5lib")
                     for i in range(amount)]
        fieldValues = {}
        # Loop through each field
        for field, fieldDic in self.adType.fields.items():
            # If the field defines how to scrap it
            if 'scrapCode' in fieldDic:
                code = fieldDic['scrapCode']
                # Get the field values in a dictionary
                fieldValues[field] = self.get_field(code, amount, bsObjects)

        # Integrate the data on a list of dictionaries
        data = []
        for index in range(amount):
            # build the data dict iterating over the acquired fields
            dataDic = {}
            for field, values in fieldValues.items():
                dataDic[field] = values[index]
            data.append(dataDic)
        return data

    def test_scrapper(self):
        self.build_accessors()
        print(self.scrap_data(20))
