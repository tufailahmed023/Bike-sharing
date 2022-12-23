import pandas as pd
import pymongo 
import json
import os
from dataclasses import dataclass


@dataclass
class Enviroment:
    mongo_db_url = os.getenv("MONGO_DB_URL")


TARGET_COLUMN = "cnt"
