from .data_base_class import DataBase
from .etecsa_data_type_classes import SQLAlchemyLandline, SQLAlchemyMobile, Phone, EtecsaBase


class EtecsaDataBase(DataBase):
    def __init__(self):
        super(EtecsaDataBase, self).__init__('etecsa')
        self.phoneType = Phone()

    def write_phone(self, phoneDic, phoneT='mobile'):
        if phoneT == 'mobile':
            phoneClass = SQLAlchemyMobile
        elif phoneT == 'landline':
            phoneClass = SQLAlchemyLandline
        else:
            return

        self.write_element('number', phoneDic,
                           self.phoneType.fields, phoneClass)

    def create_etecsa_tables(self):
        EtecsaBase.metadata.create_all(self.cursor)
