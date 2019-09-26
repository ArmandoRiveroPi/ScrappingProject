import re
import dateparser
import datetime


class Preprocessor:
    """Does several transformations to raw data fields obtained by the scrapper

    Depends on the meaning of each data field actually obtained by the scrapper and its intended meaning at the end
    Provides clean, well prepared, data fields that mean what we want, ready to store in DB, for feature extracting or model training
    """

    def __init__(self):
        self.cleanTransforms = [
            [r"\s\s+", " "],  # multiple white spaces
        ]

    def general_cleaner(self, content):
        for trans in self.cleanTransforms:
            # Apply dictionary transforms
            content = re.sub(trans[0], trans[1], content)
            # Strip newlines and whitespaces
            content = content.strip('\n *-')
        return content

    def transform_date(self, key, content):
        if key == 'datetime':
            datetime = dateparser.parse(content)
            if datetime:
                content = datetime.isoformat(sep=" ")
            else:
                content = None
        return content

    def transform_is_renewable(self, key, content):
        if key == 'is_renewable':
            content = len(content) > 10
        return content

    def transform_classification(self, key, content):
        if key == 'classification':
            content = self.classParser.get_classification(content)
        return content

    def transform_phone(self, key, content):
        if key == 'user_phone':
            content = ",".join(self.phoneParser.phone_numbers(content))
        return content

    def transform_name(self, key, content):
        if key == 'user_name':
            content = re.sub(r"[^ a-zA-Z0-9]", "", content)
        return content

    def all_transforms(self, dataDic: dict):
        """Apply all data transforms to the fields in a data dictionary

        Arguments:
            dataDic {dict} -- dictionary containing the data

        Returns:
            dict -- a dictionary with the same structure but transformed fields
        """
        for key in dataDic:
            dataDic[key] = self.general_cleaner(dataDic[key])
        # Special transforms
        dataDic['datetime'] = self.transform_date(
            'datetime', dataDic['datetime'])
        dataDic['is_renewable'] = self.transform_is_renewable(
            'is_renewable', dataDic['is_renewable'])
        dataDic['classification'] = self.transform_classification(
            'classification', dataDic['classification'])
        dataDic['user_phone'] = self.transform_phone(
            'user_phone', dataDic['user_phone'])
        dataDic['user_name'] = self.transform_name(
            'user_name', dataDic['user_name'])

        dataDic['extra_data'] = '{ "id_set":["' + dataDic['ad_id'] + \
            '"], "datetime_set": ["' + str(dataDic['datetime']) + '"] }'

        return dataDic

    def preprocess_data(self, data):
        # Create the phone parser
        self.phoneParser = PhoneParser('')
        # Create the classification parser
        self.classParser = ClassificationParser()
        # Apply all transforms
        data = [self.all_transforms(datum) for datum in data]
        return data


class PhoneParser:
    """Encapsulates the parsing of phone strings

    Depends on the way the people write phones in the phone field, and also of Cuban phone numbers format
    Provides a list of phone numbers, ideally correctly formated Cuban phone numbers
    Working with like 98% of phone numbers (getting the same number a human could)
    """

    def __init__(self, phoneString):
        self.string = phoneString
        # TODO make these transformations case insensitive
        self.initianSubs = [
            [r'\b\(|\+53(\d?)\D+', r'\1'],  # the Cuban prefix
            [r'\b\(|\+34(\d?)\D+', r'\1'],  # the Spanish prefix
            [r'\b\(|\+1(\d?)\D+', r'\1'],  # the US prefix
            [r'\b(uno|UNO)\b', '1'],  # Number 1 written with words
            [r'\b(dos|DOS)\b', '2'],  # Number 2 written with words
            [r'\b(tres|TRES)\b', '3'],  # Number 3 written with words
            [r'\b(cuatro|CUATRO)\b', '4'],  # Number 4 written with words
            [r'\b(cinco|CINCO)\b', '5'],  # Number 5 written with words
            [r'\b(seis|SEIS)\b', '6'],  # Number 6 written with words
            [r'\b(siete|SIETE)\b', '7'],  # Number 7 written with words
            [r'\b(ocho|OCHO)\b', '8'],  # Number 8 written with words
            [r'\b(nueve|NUEVE)\b', '9'],  # Number 9 written with words
            [r'\b(cero|CERO)\b', '0'],  # Number 0 written with words
            [r'[^0-9 +]+', ' '],  # anything but a +, a space or a number
            [r'\s+', ' '],  # all multiple white spaces
        ]
        self.finalSubs = [
            [r'\D', r''],  # Any not a number
        ]

    def initial_clean(self):
        for sub in self.initianSubs:
            self.string = re.sub(sub[0], sub[1], self.string)
        return self.string

    def final_clean(self, phone):
        for sub in self.finalSubs:
            phone = re.sub(sub[0], sub[1], phone)
        return phone

    def phone_numbers(self, phone=''):
        """returns the list of formated phone numbers

        Returns:
            list -- a list of phone numbers
        """
        if phone != '':
            self.string = phone
        self.initial_clean()
        numbers = [self.string]
        # Only do further processing if the string is not a block of numbers
        if not re.match(r'^\+?\d+$', self.string):
            numbers = re.findall(r"(?:\D*\d){8}", self.string)
        numbers = [self.final_clean(number) for number in numbers]
        return numbers


class ClassificationParser:
    """Cares about transforming the original raw classifications
    into our own classification system
    """

    def __init__(self):
        self.sep = " >> "

    def get_classification(self, origClass):
        # First simplify the classification representation
        origClass = self.simplify_old_class(origClass)
        # Then perform the other transformations
        newClass = origClass
        return newClass

    def simplify_old_class(self, origClass):
        parts = origClass.lower().split(self.sep)
        if len(parts) >= 3:
            origClass = parts[1] + self.sep + parts[2]
        else:
            print("Classification Error: ", origClass)
            origClass = ''
        return origClass
