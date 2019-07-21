"""This module handles the creation of users data.
Users come from ads, by mining the ads, mostly lead by
phone numbers, as they can be considered stronger signals
than names
"""
from ..DataBase import DataBase, RevoUser, Advert
from ..functions import dict_unique
import json


class UsersBuilder:
    def __init__(self, db: DataBase):
        self.db = db
        self.userClass = RevoUser()
        self.adClass = Advert()

    def build_users(self):
        # Get all ads and loop through them
        ads = self.db.get_all_ads()
        for ad in ads:
            # for each ad get a list of phone numbers
            phones = ad.user_phone.split(',')
            # get all the users that have any of these numbers
            duplicateUsers = self.find_users_with_phones(phones)
            # if no user has the numbers, create a new one
            newUser = self.create_user(ad.user_name, phones)
            if len(duplicateUsers) == 0:
                primaryUser = newUser
            else:
                # if there are users with the number
                # Merge all of these users together
                duplicateUsers.append(newUser)
                primaryUser = self.merge_users(duplicateUsers)
                # Delete the duplicates
                duplicateUsers.pop()
                self.delete_users(duplicateUsers)
            # Write the final user to the DB
            self.db.write_user(primaryUser)
            # Link the ad to the user
            adDic = self.adClass.advert_to_dic(ad)
            adDic['user'] = primaryUser['user_id']
            self.db.write_ad(adDic)
        # Count how many ads does each user has
        self.count_users_ads()

    def find_users_with_phones(self, phoneList):
        users = []
        # for each phone number find all users
        for phone in phoneList:
            if self.userClass.is_phone_good(phone):
                userObjs = self.db.find_users_by_phone(phone)
                # Append the users
                users += [self.userClass.from_obj_to_dic(userObj)
                          for userObj in userObjs if userObj]
        return dict_unique(users)

    def merge_users(self, userList):
        """Returns a merged user

        Arguments:
            userList {list} -- list of users to merge, the first is considered the primary
        """
        primary = userList.pop(0)
        # Make a reduction of the users list
        for user in userList:
            primary = self.merge_2_users(primary, user)
        return primary

    def merge_2_users(self, user1, user2):
        merged = {}
        merged['user_id'] = user1['user_id']
        if user1['name'] != '':
            merged['name'] = user1['name']
        else:
            merged['name'] = user2['name']

        merged['name_set'] = self.merge_unique_lists(
            user1['name_set'], user2['name_set'])
        merged['phone_numbers'] = self.merge_unique_lists(
            user1['phone_numbers'], user2['phone_numbers'])

        return merged

    def merge_unique_lists(self, listString1: str, listString2: str):
        list1 = listString1.split(',')
        list2 = listString2.split(',')
        mergedList = list1 + list2
        mergedList = list(set(mergedList))
        mergedList = [el for el in mergedList if el != '']
        return ','.join(mergedList)

    def delete_users(self, userList):
        """Deletes a list of users from the DB

        Intended to clean after we find two users share phone numbers
        and need to be merged

        Arguments:
            userID {string} -- ID of the user to be deleted
        """
        for user in userList:
            if 'user_id' in user:
                self.db.delete_user(user['user_id'])
        # Remember when you delete an user you need to update the ads owned by the user

    def create_user(self, name, phones):
        user = {
            'user_id': 0,
            'name': name,
            'phone_numbers': ','.join(phones),
            'name_set': name,
        }
        return user

    def count_users_ads(self):
        users = self.db.get_all_users()
        for user in users:
            # get the count of ads linked to the user
            adsCount = self.db.count_users_ads(user.user_id)
            user.ads_amount = adsCount
            userDic = self.userClass.from_obj_to_dic(user)
            self.db.write_user(userDic)
