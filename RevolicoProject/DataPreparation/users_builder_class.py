"""This module handles the creation of users data.
Users come from ads, by mining the ads, mostly lead by
phone numbers, as they can be considered stronger signals
than names
"""
from ..DataBase import DataBase, RevoUser


class UsersBuilder:
    def __init__(self, db: DataBase):
        self.db = db
        self.userClass = RevoUser()

    def build_users(self):
        # Get all ads and loop through them
        ads = self.db.get_all_ads()
        for ad in ads:
            # for each ad get a list of phone numbers
            phones = ad.user_phone.split(',')
            users = self.find_users_with_phones(phones)
            print(phones, users)
            # get all the users that have any of these numbers
            # if no user has the numbers, create a new one
            # if there are users with the number
            # Merge all of these users together
            # Write the merged user to the DB
            # Delete the duplicates
        pass

    def find_users_with_phones(self, phoneList):
        users = []
        # for each phone number find all users
        for phone in phoneList:
            userObjs = self.db.find_users_by_phone(phone)
            # Append the users
            users += [self.userClass.from_obj_to_dic(userObj)
                      for userObj in userObjs]
        return users

    def merge_users(self, userList):
        """Returns a merged user

        Arguments:
            userList {list} -- list of users to merge, the first is considered the primary
        """
        pass

    def delete_user(self, userID):
        """Deletes a user

        Intended to clean after we find two users share phone numbers
        and need to be merged

        Arguments:
            userID {string} -- ID of the user to be deleted
        """
        pass
