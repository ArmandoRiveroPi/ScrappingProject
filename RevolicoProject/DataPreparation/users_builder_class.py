"""This module handles the creation of users data.
Users come from ads, by mining the ads, mostly lead by
phone numbers, as they can be considered stronger signals
than names
"""


class UsersBuilder:
    def __init__(self, parameter_list):
        pass

    def build_users(self, parameter_list):
        pass

    def find_users_with_phone(self, parameter_list):
        pass

    def merge_users(self, user1, user2):
        """Returns a merged user

        Arguments:
            user1 {RevoUser} -- first user to merge
            user2 {RevoUser} -- second user to merge
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
