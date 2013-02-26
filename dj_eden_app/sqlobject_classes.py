from sqlobject import *
from sqlobject.mysql import builder
from sqlobject.util.csvexport import export_csv

from secure import *

conn = builder()(user=DB_USER,
                 password=DB_PASSWORD,
                 host=DB_HOST,
                 db=DB_SCHEMA)

class Stage(SQLObject):
    
    _connection = conn
    datetime = DateTimeCol()
       
    class sqlmeta:
        idName = 'datetime'
        idType = str
        fromDatabase = True
        table = 'Stage'
        style = MixedCaseStyle(longID=True)
        