import pandas as pd
import pymongo 
import json
import os
from dataclasses import dataclass


@dataclass
class Enviroment:
    mongo_db_url = os.getenv("MONGO_DB_URL")


evr = Enviroment()
client =  pymongo.MongoClient(evr.mongo_db_url)


TARGET_COLUMN = "cnt"
countinous_columns = ["temp","atemp","hum","windspeed"]
columns_to_convert = ["season","mnth","weekday","weathersit"]
to_convert_data = {'mnth' : {1:"jan",2:"feb",3:"mar",4:"apr",5:'may',6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"},
                    "weathersit" :{1 : 'good' ,2 : 'modrate',3 : 'bad' },
                    'season' : {1 : 'spring',2 : 'summer',3 : 'fall',4 : 'winter'},
                    'weekday' : {0: 'sun',1: 'mon',2: 'tue',3: 'wed',4: 'thu',5: 'fri',6: 'sat'}
                    }
