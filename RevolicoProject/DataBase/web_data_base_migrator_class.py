"""This module is concerned with creating the webserver database
from the model training data.

Because of that, it depends both in knowing and probably connecting
with both databases.
It should provide a web server database ready for the server to use.
"""
from .data_base_class import DataBase
from sqlalchemy import MetaData, Table, Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func as sql_func, asc as sql_asc
import re
# You have to make all the db operations under this same base,
# otherwise the ORM might not work properly
DeclarativeBase = declarative_base()


class WebAdvert(DeclarativeBase):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'revolico_ads'

    ad_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    bperson_name = Column(String)
    price = Column(String)
    classification = Column(String)
    # # relationship("WebBperson", back_populates='adverts')
    bperson_id = Column(Integer, ForeignKey('revolico_bperson.bperson_id'))
    phone = Column(String)  # Coma separated list of phone numbers
    datetime = Column(DateTime)


class WebBperson(DeclarativeBase):
    """Class to represent an advert to the SQLAlchemy ORM

    Arguments:
        base {object} -- declarative_base() built object to inherit from
    """
    __tablename__ = 'revolico_bperson'

    bperson_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    name_set = Column(Text)
    adverts = relationship("WebAdvert")
    ads_amount = Column(Integer)


class WebDataBase:
    """Main class to encapsulate the DB functionality

    Right now mostly relying on SQL Alchemy
    """

    def __init__(self, dbName='revolico_web'):
        self.user = 'postgres'
        self.dbName = dbName
        self.password = 'root'
        self.host = 'localhost:5432'
        self.dbString = "postgres://{user}:{password}@{host}/{db}".format(
            user=self.user, password=self.password, host=self.host, db=self.dbName)
        self.cursor = create_engine(self.dbString)
        self.session = sessionmaker(self.cursor)()
        self.adType = WebAdvert()
        self.bpersonType = WebBperson()
    # ------ GENERAL SECTION -----------

    def write_element(self, idName, elem, fields, elemClass):
        elemID = getattr(elem, idName)
        # If the ID is cero, auto increment it
        if elemID == 0:
            try:
                elemID = self.session.query(sql_func.max(
                    getattr(elemClass, idName))).scalar() + 1
            except TypeError:
                elemID = 1
            setattr(elem, idName, elemID)

        # Try to get the element by ID
        oldElem = self.session.query(elemClass).get(elemID)
        # If the element exists only modify it
        if oldElem:
            for field in fields:
                setattr(oldElem, field, getattr(elem, field))
        else:
            # If the element doesn't exist, you need to add it
            self.session.add(elem)

        self.session.commit()

    def get_all_elements(self, elementClass):
        elements = self.session.query(elementClass).all()
        return elements

    def get_element_by_id(self, elemID, elemClass):
        return self.session.query(elemClass).get(elemID)

    def delete_element(self, elemID, elementClass):
        if int(elemID) != 0:
            elem = self.session.query(elementClass).get(elemID)
            self.session.delete(elem)

    # ----- SECTION FOR ADS -------------

    def write_ad(self, advert: WebAdvert):
        fields = ['ad_id', 'title', 'content', 'bperson_name', 'bperson_id',
                  'phone', 'classification', 'price', 'datetime']
        self.write_element('ad_id', advert, fields, WebAdvert)

    # def write_ads(self, adList: list):
    #     for ad in adList:
    #         self.write_ad(ad)

    # def advert_to_dic(self, adObj: WebAdvert):
    #     adDic = {}
    #     for field in self.adType.fields:
    #         adDic[field] = getattr(adObj, field)
    #     return adDic

    def get_all_ads(self):
        return self.get_all_elements(WebAdvert)

    # def get_ad_by_id(self, adID):
    #     return self.get_element_by_id(adID, WebAdvert)

    # def delete_ad(self, adID):
    #     self.delete_element(adID, WebAdvert)
    # ---------- SECTION FOR BpersonS ------------

    def get_all_bpersons(self):
        return self.get_all_elements(WebBperson)

    # def get_bperson_by_id(self, bpersonID):
    #     return self.get_element_by_id(bpersonID, WebBperson)

    def write_bperson(self, bperson: WebBperson):
        fields = ['bperson_id', 'name', 'phone', 'name_set', 'ads_amount']
        self.write_element('bperson_id', bperson, fields, WebBperson)

    def find_bperson_by_phone(self, phone):
        bpersonsWithPhone = self.session.query(WebBperson).filter(
            WebBperson.phone.like('%' + phone + '%')).order_by('bperson_id')
        return bpersonsWithPhone

    def delete_bperson(self, bpersonID):
        self.delete_element(bpersonID, WebBperson)

    # def get_bpersons_ads(self, bpersonID):
    #     ads = self.session.query(WebAdvert).join(
    #         WebBperson).filter(WebBperson.bperson_id == bpersonID).all()
    #     return ads

    def count_bpersons_ads(self, bpersonID):
        adsAmount = self.session.query(WebAdvert).join(
            WebBperson).filter(WebBperson.bperson_id == bpersonID).count()
        return adsAmount


class WebDataBaseMigrator(object):

    def __init__(self, trainDB: DataBase, webDB: WebDataBase):
        self.trainDB = trainDB
        self.webDB = webDB

    def migrate_ads(self, amount=10):
        ads = self.trainDB.get_all_ads()
        counter = 0
        for ad in ads:
            if amount > 0 and counter >= amount:
                break
            counter += 1
            self.migrate_ad(ad.ad_id)

    def migrate_ad(self, adID):
        """Read an ad from the Train DB and copy it to the Web DB
        """
        trainAd = self.trainDB.get_ad_by_id(adID)
        # Try to get the element by ID
        # oldAd = self.webDB.session.query(WebAdvert).get(adID)
        # self.webDB.write_ad(oldAd)
        newAd = WebAdvert()
        fields = {
            'ad_id': 'ad_id',
            'title': 'title',
            'content': 'content',
            'bperson_name': 'user_name',
            # 'bperson_id': 'user',
            'phone': 'user_phone',
            'classification': 'classification',
            'price': 'price',
            'datetime': 'datetime'
        }
        for field in fields:
            setattr(newAd, field, getattr(trainAd, fields[field]))
        self.webDB.write_ad(newAd)
        # If the element exists only modify it
        # if oldAd:
        #     oldAd.title = trainAd.title
        #     oldAd.content = trainAd.content
        #     oldAd.phone = trainAd.phone
        # else:
        #     # If the element doesn't exist, you need to add it
        #     newAd = WebAdvert()
        #     newAd.ad_id = adID
        #     newAd.title = trainAd.title
        #     newAd.content = trainAd.content
        #     newAd.phone = trainAd.phone
        #     self.webDB.session.add(newAd)
        # self.webDB.session.commit()

    def build_bpersons(self):
        # Get all ads and loop through them
        ads = self.webDB.get_all_ads()
        counter = 0
        for ad in ads:
            # for each ad get a list of phone numbers
            phones = ad.phone.split(',')
            # get all the bpersons that have any of these numbers
            duplicateBpersons = self.find_bpersons_with_phones(phones)
            # if no bperson has the numbers, create a new one
            newBperson = self.create_bperson(ad.bperson_name, phones)
            if len(duplicateBpersons) == 0:
                primaryBperson = newBperson
            else:
                # if there are bpersons with the number
                # Merge all of these bpersons together
                duplicateBpersons.append(newBperson)
                primaryBperson = self.merge_bpersons(duplicateBpersons)
                # Delete the duplicates
                duplicateBpersons.pop()
                self.delete_bpersons(duplicateBpersons)
            # Write the final bperson to the DB
            self.webDB.write_bperson(primaryBperson)
            # Link the ad to the bperson
            ad.bperson_id = primaryBperson.bperson_id
            self.webDB.write_ad(ad)

            counter += 1
            if counter % 1000 == 0:
                print('Created bperson for ad #', counter)
        # Count how many ads does each bperson has
        self.count_bpersons_ads()

    def find_bpersons_with_phones(self, phoneList):
        bpersons = []
        # for each phone number find all bpersons
        for phone in phoneList:
            if re.match(r'\d{8,}', phone):
                bpersonObjs = self.webDB.find_bperson_by_phone(phone)
                # Append the bpersons
                bpersons += bpersonObjs
        return list(set(bpersons))

    def merge_bpersons(self, bpersonList):
        """Returns a merged bperson

        Arguments:
            bpersonList {list} -- list of bpersons to merge, the first is considered the primary
        """
        primary = bpersonList.pop(0)
        # Make a reduction of the bpersons list
        for bperson in bpersonList:
            primary = self.merge_2_bpersons(primary, bperson)
        return primary

    def merge_2_bpersons(self, bperson1, bperson2):
        merged = WebBperson()
        merged.bperson_id = bperson1.bperson_id
        if bperson1.name != '':
            merged.name = bperson1.name
        else:
            merged.name = bperson2.name

        merged.name_set = self.merge_unique_lists(
            bperson1.name_set, bperson2.name_set)
        merged.phone = self.merge_unique_lists(
            bperson1.phone, bperson2.phone)

        return merged

    def merge_unique_lists(self, listString1: str, listString2: str):
        list1 = listString1.split(',')
        list2 = listString2.split(',')
        mergedList = list1 + list2
        mergedList = list(set(mergedList))
        mergedList = [el for el in mergedList if el != '']
        return ','.join(mergedList)

    def delete_bpersons(self, bpersonList):
        """Deletes a list of bpersons from the DB

        Intended to clean after we find two bpersons share phone numbers
        and need to be merged

        Arguments:
            bpersonID {string} -- ID of the bperson to be deleted
        """
        for bperson in bpersonList:
            if getattr(bperson, 'bperson_id'):
                self.webDB.delete_bperson(bperson.bperson_id)
        # Remember when you delete an bperson you need to update the ads owned by the bperson

    def create_bperson(self, name, phones):
        # bperson = {
        #     'bperson_id': 0,
        #     'name': name,
        #     'phone_numbers': ','.join(phones),
        #     'name_set': name,
        # }
        bperson = WebBperson()
        bperson.bperson_id = 0
        bperson.name = name
        bperson.phone = ','.join(phones)
        bperson.name_set = name
        return bperson

    def count_bpersons_ads(self):
        bpersons = self.webDB.get_all_bpersons()
        for bperson in bpersons:
            # get the count of ads linked to the bperson
            adsCount = self.webDB.count_bpersons_ads(bperson.bperson_id)
            bperson.ads_amount = adsCount
            self.webDB.write_bperson(bperson)
