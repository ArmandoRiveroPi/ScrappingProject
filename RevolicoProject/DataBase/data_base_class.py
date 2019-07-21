from .data_type_classes import RevoUser, Advert, SQLAlchemyAdvert, SQLAlchemyUser, DeclarativeBase
from sqlalchemy import create_engine, func as sql_func, asc as sql_asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import re
from datetime import datetime
import json

# base = declarative_base()


class DataBase:
    """Main class to encapsulate the DB functionality

    Right now mostly relying on SQL Alchemy
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
    def write_element(self, idName, elemData, elemFields, elemClass):
        # Set the fields to their defaults in case they don't exist
        for field, fieldInfo in elemFields.items():
            if not field in elemData:
                elemData[field] = fieldInfo['default']

        DeclarativeBase.metadata.create_all(self.cursor)
        # If the ID is cero, auto increment it
        elemID = int(elemData[idName])
        if elemID == 0:
            try:
                elemID = self.session.query(sql_func.max(
                    getattr(elemClass, idName))).scalar() + 1
            except TypeError:
                elemID = 1
            elemData[idName] = elemID

        # Try to get the element by ID
        oldElem = self.session.query(elemClass).get(elemID)
        newElem = elemClass()
        # If the element exists only modify it
        if oldElem:
            for field in elemFields:
                setattr(oldElem, field, elemData[field])
        else:
            # If the element doesn't exist, you need to add it
            for field in elemFields:
                setattr(newElem, field, elemData[field])
            self.session.add(newElem)

        self.session.commit()

    def get_all_elements(self, elementClass):
        elements = self.session.query(elementClass).all()
        return elements

    def create_tables(self):
        DeclarativeBase.metadata.create_all(self.cursor)

    def delete_element(self, elemID, elementClass):
        if int(elemID) != 0:
            elem = self.session.query(elementClass).get(elemID)
            self.session.delete(elem)

    # ----- SECTION FOR ADS -------------

    def find_ads_by_title(self, title: str):
        ads = self.session.query(SQLAlchemyAdvert).filter(
            SQLAlchemyAdvert.title == title)
        adDicts = []
        if ads:
            adDicts = [self.advert_to_dic(ad) for ad in ads]
        return adDicts

    def write_ad(self, adDic: dict):
        # End early if the ID doesn't have a good format
        if not self.goodID.match(str(adDic['ad_id'])):
            return

        self.write_element('ad_id', adDic,
                           self.adType.fields, SQLAlchemyAdvert)

    def write_ads(self, adList: list):
        for ad in adList:
            self.write_ad(ad)

    def advert_to_dic(self, adObj: SQLAlchemyAdvert):
        adDic = {}
        for field in self.adType.fields:
            adDic[field] = getattr(adObj, field)
        return adDic

    def get_all_ads(self):
        return self.get_all_elements(SQLAlchemyAdvert)

    def delete_ad(self, adID):
        self.delete_element(adID, SQLAlchemyAdvert)
    # ---------- SECTION FOR USERS ------------

    def get_all_users(self):
        return self.get_all_elements(SQLAlchemyUser)

    def write_user(self, userDic):
        self.write_element('user_id', userDic,
                           self.userType.fields, SQLAlchemyUser)

    def find_users_by_phone(self, phone):
        usersWithPhone = self.session.query(SQLAlchemyUser).filter(
            SQLAlchemyUser.phone_numbers.like('%' + phone + '%')).order_by('user_id')
        return usersWithPhone

    def delete_user(self, userID):
        self.delete_element(userID, SQLAlchemyUser)

    def get_users_ads(self, userID):
        ads = self.session.query(SQLAlchemyAdvert).join(
            SQLAlchemyUser).filter(SQLAlchemyUser.user_id == userID).all()
        return ads

    def count_users_ads(self, userID):
        adsAmount = self.session.query(SQLAlchemyAdvert).join(
            SQLAlchemyUser).filter(SQLAlchemyUser.user_id == userID).count()
        return adsAmount
