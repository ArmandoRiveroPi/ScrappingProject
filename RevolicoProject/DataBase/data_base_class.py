from .advert_class import SQLAlchemyAdvert, Advert, AdsTable
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
from datetime import datetime
import json

base = declarative_base()


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

    def create_ads_table(self):
        adTb = AdsTable(self.dbString)
        adTb.table.create()

    def find_ads_by_title(self, title: str):
        ads = self.session.query(SQLAlchemyAdvert).filter(
            SQLAlchemyAdvert.title == title)
        adDicts = []
        if ads:
            adDicts = [self.advert_to_dic(ad) for ad in ads]
        return adDicts

    def read_ad(self, adID):
        # End early if the ID doesn't have a good format
        if not self.goodID.match(adID):
            return

        results = self.cursor.execute(
            "SELECT * FROM ads WHERE ad_id = {ad_id};".format(ad_id=adID))
        ads = self.rows_to_ads(results)
        if len(ads):
            return ads[0]
        else:
            return None

    def write_ad(self, adDic: dict):
        # End early if the ID doesn't have a good format
        if not self.goodID.match(str(adDic['ad_id'])):
            return

        # Set the fields to their defaults in case they don't exist
        for field, fieldInfo in self.adType.fields.items():
            if not field in adDic:
                adDic[field] = fieldInfo['default']

        base.metadata.create_all(self.cursor)
        # Try to get the ad by ID
        oldAdvert = self.session.query(SQLAlchemyAdvert).get(adDic['ad_id'])
        newAdvert = SQLAlchemyAdvert()
        # If the ad exists only modify it
        if oldAdvert:
            for field in self.adType.fields:
                setattr(oldAdvert, field, adDic[field])
        else:
            # If the ad doesn't exist, you need to add it
            for field in self.adType.fields:
                setattr(newAdvert, field, adDic[field])
            self.session.add(newAdvert)

        self.session.commit()

    def write_ads(self, adList: list):
        for ad in adList:
            self.write_ad(ad)

    def rows_to_ads(self, rows: list):
        ads = [{'ad_id': row[0], 'title':row[1]} for row in rows]
        return ads

    def advert_to_dic(self, adObj: SQLAlchemyAdvert):
        adDic = {}
        for field in self.adType.fields:
            adDic[field] = getattr(adObj, field)
        return adDic
