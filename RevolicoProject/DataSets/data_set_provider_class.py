"""This module provides the base for data set access
"""


class DataSetProvider(object):
    """Encapsulates basic data set access functionality

    It's meant to be the base class for specific data sets
    """

    def __init__(self, dataAmount=0, testIDFile='', isTest=False):
        # Percent of the data to be included in the test set
        self.testPart = 0.2
        # A list of the IDs to be included on the test set
        self.testIDs = []
        # How many elements should be available
        self.amount = dataAmount
        # Whether the data set is train or test
        self.isTest = isTest

    def get_all_data(self):
        """Gets an array of all data in the dataset
        """
        pass

    def get_data_by_index(self, index):
        """Gets a datum given by some dataset index

        Arguments:
            index {int} -- location of the datum in the dataset
        """
        pass

    # ----------  TEST IDS SECTION ---------------------
    def build_test_ids(self):
        """Creates a list of random IDs up to some percent to be used as test set
        """
        # Get all the ids of data elements
        # The total times the fraction of test elements is the
        # amount of test elements
        # Take a random sample of test elements from the list
        pass

    def expand_test_set_ids(self, parameter_list):
        """Adds new IDs to the test set ids

        To be used after the whole data set is expanded and we need more
        elements in the test set to reach the test set fraction
        """
        # Find the highest ID in the test set
        # from the data with ID higher than that
        # make a random sample of the amount needed to reach the fraction
        pass

    def save_test_ids(self, idFile=''):
        """Saves the test ids, as they should be kept constant
        """
        pass

    def read_test_ids(self, idFile=''):
        """Reads the test ids for further use or expansion
        """
        # If the file name is not empty
        # Try to read from the file,
        # If the file doesn't exist or is empty,
        # build the test ids and write them to the same file name
        pass

    def is_test_id(self, elemID):
        """Tells whether the ID belongs to a test set datum

        Arguments:
            elemID {int|string} -- id of the element to be checked

        Returns:
            [bool] -- whether the element belongs to the test set
        """
        return False
