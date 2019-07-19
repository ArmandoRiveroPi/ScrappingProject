from .data_type_classes import RevoUser, UsersTable, Advert, AdsTable, SQLAlchemyAdvert, SQLAlchemyUser, DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import re
from datetime import datetime
import json

# base = declarative_base()


class DataBase:
    """Main class to encapsulate the DB functionality
    """

    def __init__(self):
        self.user = 'postgres'
        self.dbName = 'revolico'
        self.password = 'root'
        self.host = 'localhost:5432'
        self.dbString = "postgres://{user}:{password}@{host}/{db}".format(
            user=self.user, password=self.password, host=self.host, db=self.dbName)
        self.cursor = create_engine(self.dbString)
        self.session = sessionmaker(self.cursor)()
        self.goodID = re.compile(r'\d{8,}')
        self.adType = Advert()
        self.userType = RevoUser()

    # ------ GENERAL SECTION -----------
    def write_element(self, elemID, elemData, elemFields, elemClass):
        # Set the fields to their defaults in case they don't exist
        for field, fieldInfo in elemFields.items():
            if not field in elemData:
                elemData[field] = fieldInfo['default']

        DeclarativeBase.metadata.create_all(self.cursor)
        # Try to get the element by ID
        oldElem = self.session.query(elemClass).get(elemID)
        newElem = elemClass()
        # If the element exists only modify it
        if oldElem:
            for field in elemFields:
                setattr(oldElem, field, elemData[field])
        else:
            # If the ad doesn't exist, you need to add it
            for field in elemFields:
                setattr(newElem, field, elemData[field])
            self.session.add(newElem)

        self.session.commit()

    def get_all_elements(self, elementClass):
        elements = self.session.query(elementClass).all()
        return elements

    def create_tables(self):
        DeclarativeBase.metadata.create_all(self.cursor)

    # ----- SECTION FOR ADS -------------
    def create_ads_table(self):
        try:
            adTb = AdsTable(self.dbString)
            adTb.table.create()
        except:
            pass

    def find_ads_by_title(self, title: str):
        ads = self.session.query(SQLAlchemyAdvert).filter(
            SQLAlchemyAdvert.title == title)
        adDicts = []
        if ads:
            adDicts = [self.advert_to_dic(ad) for ad in ads]
        return adDicts

    # def read_ad(self, adID):
    #     # End early if the ID doesn't have a good format
    #     if not self.goodID.match(adID):
    #         return

    #     results = self.cursor.execute(
    #         "SELECT * FROM ads WHERE ad_id = {ad_id};".format(ad_id=adID))
    #     ads = self.rows_to_ads(results)
    #     if len(ads):
    #         return ads[0]
    #     else:
    #         return None

    def write_ad(self, adDic: dict):
        # End early if the ID doesn't have a good format
        if not self.goodID.match(str(adDic['ad_id'])):
            return

        self.write_element(adDic['ad_id'], adDic,
                           self.adType.fields, SQLAlchemyAdvert)

        # # Set the fields to their defaults in case they don't exist
        # for field, fieldInfo in self.adType.fields.items():
        #     if not field in adDic:
        #         adDic[field] = fieldInfo['default']

        # base.metadata.create_all(self.cursor)
        # # Try to get the ad by ID
        # oldAdvert = self.session.query(SQLAlchemyAdvert).get(adDic['ad_id'])
        # newAdvert = SQLAlchemyAdvert()
        # # If the ad exists only modify it
        # if oldAdvert:
        #     for field in self.adType.fields:
        #         setattr(oldAdvert, field, adDic[field])
        # else:
        #     # If the ad doesn't exist, you need to add it
        #     for field in self.adType.fields:
        #         setattr(newAdvert, field, adDic[field])
        #     self.session.add(newAdvert)

        # self.session.commit()

    def write_ads(self, adList: list):
        for ad in adList:
            self.write_ad(ad)

    # def rows_to_ads(self, rows: list):
    #     ads = [{'ad_id': row[0], 'title':row[1]} for row in rows]
    #     return ads

    def advert_to_dic(self, adObj: SQLAlchemyAdvert):
        adDic = {}
        for field in self.adType.fields:
            adDic[field] = getattr(adObj, field)
        return adDic

    def get_all_ads(self):
        return self.get_all_elements(SQLAlchemyAdvert)

    # ---------- SECTION FOR USERS ------------
    def create_users_table(self):
        try:
            usersTb = UsersTable(self.dbString)
            usersTb.table.create()
        except:
            pass

    def get_all_users(self):
        return self.get_all_elements(SQLAlchemyUser)

    def write_user(self, userDic):
        self.write_element(userDic['user_id'], userDic,
                           self.userType.fields, SQLAlchemyUser)

    def find_users_by_phone(self, phone):
        usersWithPhone = self.session.query(SQLAlchemyUser).filter(
            SQLAlchemyUser.phone_numbers.like('%' + phone + '%'))
        return usersWithPhone
