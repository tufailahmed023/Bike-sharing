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
columns_to_drop = ['instant','dteday',"casual",	"registered"]
countinous_columns = ["temp","atemp","hum","windspeed"]
columns_to_convert = ["season","mnth","weekday","weathersit"]
to_convert_data = {'mnth' : {1:"jan",2:"feb",3:"mar",4:"apr",5:'may',6:"jun",7:"jul",8:"aug",9:"sep",10:"oct",11:"nov",12:"dec"},
                    "weathersit" :{1 : 'good' ,2 : 'modrate',3 : 'bad' },
                    'season' : {1 : 'spring',2 : 'summer',3 : 'fall',4 : 'winter'},
                    'weekday' : {0: 'sun',1: 'mon',2: 'tue',3: 'wed',4: 'thu',5: 'fri',6: 'sat'}
                    }



Months = {
'January': [0,0,0,0,1,0,0,0,0,0,0,0],
'February': [0,0,0,1,0,0,0,0,0,0,0,0],
'March': [0,0,0,0,0,0,0,1,0,0,0,0],
'April' : [1,0,0,0,0,0,0,0,0,0,0,0],
'May' : [0,0,0,0,0,0,0,0,1,0,0,0],
'June' : [0,0,0,0,0,0,1,0,0,0,0,0],
'July': [0,0,0,0,0,1,0,0,0,0,0,0],
'August': [0,1,0,0,0,0,0,0,0,0,0,0],
'September' : [0,0,0,0,0,0,0,0,0,0,0,1],
'October': [0,0,0,0,0,0,0,0,0,0,0,1],
'November' : [0,0,0,0,0,0,0,0,0,1,0,0],
'December' : [0,0,1,0,0,0,0,0,0,0,0,0] 
}


Season = {"Fall" : [1,0,0,0],
           "Sprint":[0,1,0,0],
           "Summer" : [0,0,1,0],
           "Winter" : [0,0,0,1]
}


Weekday = {
    "Monday" : [0,1,0,0,0,0,0],
    "Tuesday" :  [0,0,0,0,0,1,0],
    "Wednesday" : [0,0,0,0,0,0,1],
    "Thursday" : [0,0,0,0,1,0,0],
    "Friday" : [1,0,0,0,0,0,0],
    "Saturday" : [0,0,1,0,0,0,0],
    "Sunday" : [0,0,0,1,0,0,0]
}


Weather = {
    "Good" : [0,1,0],
    "Modrate" : [0,0,1],
    "Bad" : [1,0,0]
}