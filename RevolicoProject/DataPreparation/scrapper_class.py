from bs4 import BeautifulSoup


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
        fields = []
        if amount == 0:
            amount = len(self.accessors)
        for index in range(amount):
            if len(bsObjects) > index:
                soup = bsObjects[index]
            else:
                soup = BeautifulSoup(
                    self.accessors[index].get_content(), features="html5lib")
            fields.append(eval('soup.' + bsCode))
        return fields

    def get_titles(self, amount=0, bsObjects=[]):
        titles = self.get_field('h1.get_text()', amount, bsObjects)
        return titles

    def scrap_data(self, amount=0):
        # Build bs objects
        bsObjects = [BeautifulSoup(self.accessors[i].get_content(), features="html5lib")
                     for i in range(amount)]
        # Scrap each field
        titles = self.get_titles(amount, bsObjects)
        # Integrate on a data dictionary
        data = []
        for index in range(amount):
            data.append(
                {
                    "title": titles[index]
                }
            )
        return data

    def test_scrapper(self):
        self.build_accessors()
        print(self.scrap_data(20))
