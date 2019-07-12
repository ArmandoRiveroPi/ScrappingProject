from bs4 import BeautifulSoup
import re


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

    def build_accessors(self):
        self.accessors = self.provider.get_file_accessors()
        return self.accessors

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
            fieldData.append(str(eval('soup.' + bsCode)))
        return fieldData

    def scrap_data(self, amount=0):
        """Scraps some amount of files for all the fields

        Keyword Arguments:
            amount {int} -- how many files to scrap (default: {0})

        Returns:
            [list] -- list of dictionaries with the fields scrapped and their values
        """
        # Build bs objects
        bsObjects = [BeautifulSoup(self.accessors[i].get_content(), features="html5lib")
                     for i in range(amount)]
        # Define how to scrap each field (by a code bs will use)
        fieldCodes = {
            "id": 'find(text=re.compile(".*Id:")).parent.nextSibling.nextSibling.get_text()',
            "title": 'h1.get_text()',
            "content": 'find("span", class_="showAdText").get_text()',
            "datetime": 'find(text=re.compile(".*Fecha:")).parent.nextSibling.nextSibling.get_text()',
            "user_name": 'find(text=re.compile(".*Nombre:")).parent.nextSibling.nextSibling.get_text()',
            "user_phone": 'find(text=re.compile(".*fono:")).parent.nextSibling.nextSibling.get_text()',
            "classification": 'find(id="pathaway").get_text()',
            "is_renewable": 'find(id="auto_renew_hint")',
        }
        fieldValues = {}
        # Loop through each field
        for field, code in fieldCodes.items():
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
