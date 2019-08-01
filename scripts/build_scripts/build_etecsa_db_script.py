import time
# from RevolicoProject.DataBase import DataBase
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from RevolicoProject.DataBase import SQLAlchemyLandline, SQLAlchemyMobile, EtecsaDataBase, Phone

start = time.time()
base = declarative_base()

sqliteEng = create_engine(
    'sqlite:////home/gauss/arm/importante/work/ai/projects/revolico/guiaEtecsa/etecsa1.db')

meta = MetaData()
connector = sqliteEng.connect()


movilFrom = Table(
    'movil', meta,
    Column('number', Integer, primary_key=True),
    Column('name', String),
    Column('identification', String),
    Column('address', Text),
    Column('province', Integer),
)
fixFrom = Table(
    'fix', meta,
    Column('number', Integer, primary_key=True),
    Column('name', String),
    Column('address', Text),
    Column('province', Integer),
)


class MovilLite(base):
    """Class to represent an mobile phone from etecsa sqlite db to the SQLAlchemy ORM

    """
    __tablename__ = 'movil'

    number = Column(Integer, primary_key=True)
    name = Column(String)
    identification = Column(String)
    address = Column(Text)
    province = Column(Integer)


class FixLite(base):
    """Class to represent an mobile phone from etecsa sqlite db to the SQLAlchemy ORM

    """
    __tablename__ = 'fix'

    rowid = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String)
    address = Column(Text)
    province = Column(Integer)


# sel = select([movilFrom]).where(movilFrom.c.number == '5355108628')
# result = connector.execute(sel)
session = sessionmaker(sqliteEng)()

mobileAmount = session.query(MovilLite).count()
landlineAmount = session.query(FixLite).count()
print('Amount Mobile:   ', mobileAmount)
print('Amount Landline: ', landlineAmount)

phoneType = Phone()
etecsaDB = EtecsaDataBase()
etecsaDB.create_etecsa_tables()

chunkSize = 1000
mobChunks = int(mobileAmount/chunkSize) + 1
landChunks = int(landlineAmount/chunkSize) + 1
mobStart = 280
landStart = 158

# for chunk in range(mobStart, mobChunks):
#     timeStart = time.time()
#     # mobileResult = session.query(MovilLite).limit(chunkSize).all()
#     mobileResult = session.query(MovilLite).slice(
#         chunk * chunkSize, (chunk + 1) * chunkSize).all()
#     for movil in mobileResult:
#         phoneDic = phoneType.from_obj_to_dic(movil)
#         etecsaDB.write_phone(phoneDic, 'mobile')
#         # session.delete(movil)
#         # session.commit()
#     timeEnd = time.time()
#     duration = round(timeEnd - timeStart, 2)
#     speed = round(chunkSize/duration, 2)
#     print('Mobile Chunk ', chunk + 1, 'out of', mobChunks, 'in', duration,
#           'seconds, at', speed, 'items/s')

for chunk in range(landStart, landChunks):
    timeStart = time.time()
    fixResult = session.query(FixLite).limit(chunkSize).slice(
        chunk * chunkSize, (chunk + 1) * chunkSize).all()
    for landline in fixResult:
        try:
            landline.number = int(
                str(landline.province) + str(landline.number))
            phoneDic = phoneType.from_obj_to_dic(landline)
            etecsaDB.write_phone(phoneDic, 'landline')
        except ValueError:
            pass
        # session.delete(landline)
        # session.commit()
    timeEnd = time.time()
    duration = round(timeEnd - timeStart, 2)
    speed = round(chunkSize/duration, 2)
    print('Landline Chunk ', chunk + 1, 'out of', landChunks, 'in', duration,
          'seconds, at', speed, 'items/s')


end = time.time()

print('Took ' + str(round(end - start)) + ' seconds total')
