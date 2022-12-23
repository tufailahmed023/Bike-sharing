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
