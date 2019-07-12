import re
import dateparser
import datetime


class Preprocessor:
    """Does several transformations to raw data fields obtained by the scrapper

    Depends on the meaning of each data field actually obtained by the scrapper and its intended meaning at the end
    Provides clean, well prepared, data fields that mean what we want, ready to store in DB, for feature extracting or model training
    """

    def __init__(self):
        self.cleanTransforms = {
            "\s\s+": " ",  # multiple white spaces
        }

    def general_cleaner(self, content):
        for key in self.cleanTransforms:
            # Apply dictionary transforms
            content = re.sub(key, self.cleanTransforms[key], content)
            # Strip newlines and whitespaces
            content = content.strip('\n ')
        return content

    def transform_date(self, key, content):
        if key == 'datetime':
            datetime = dateparser.parse(content)
            content = datetime.isoformat(sep=" ")
        return content

    def transform_is_renewable(self, key, content):
        if key == 'is_renewable':
            content = len(content) > 10
        return content

    def transform_classification(self, key, content):
        if key == 'classification':
            sep = ' >> '
            parts = content.lower().split(sep)
            content = parts[1] + sep + parts[2]
        return content

    def transform_phone(self, key, content):
        if key == 'user_phone':
            parser = PhoneParser(content)
            content = " ".join(parser.phone_numbers())
        return content

    def all_transforms(self, dataDic):
        """Apply all data transforms to the fields in a data dictionary

        Arguments:
            dataDic {dict} -- dictionary containing the data

        Returns:
            dict -- a dictionary with the same structure but transformed fields
        """
        for key in dataDic:
            dataDic[key] = self.general_cleaner(dataDic[key])
            if key == 'datetime':
                dataDic[key] = self.transform_date(key, dataDic[key])
            if key == 'is_renewable':
                dataDic[key] = self.transform_is_renewable(key, dataDic[key])
            if key == 'classification':
                dataDic[key] = self.transform_classification(key, dataDic[key])

        return dataDic

    def preprocess_data(self, data):
        # Apply all transforms
        data = [self.all_transforms(datum) for datum in data]
        return data


class PhoneParser:
    """Encapsulates the parsing of phone strings

    Depends on the way the people write phones in the phone field, and also of Cuban phone numbers format
    Provides a list of phone numbers, ideally correctly formated Cuban phone numbers
    """

    def __init__(self, phoneString):
        self.string = phoneString

    def phone_numbers(self):
        """returns the list of formated phone numbers

        Returns:
            list -- a list of phone numbers
        """
        return [self.string]
