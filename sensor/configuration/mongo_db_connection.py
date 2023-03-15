
import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()
import os

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = "mongodb+srv://ravi0dubey:Logiw@cluster0.0zxmnkl.mongodb.net/?retryWrites=true&w=majority"
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e


        

# class MongoDBClient:
#     client = None
#     def __init__(self,database_name = DATABASE_NAME) -> None:
#         try:
#             if MongoDBClient.client is None:
#                 print("inside if")
#                 mongo_db_url = os.getenv(MONGO_DB_URL) 
#                 if mongo_db_url is None:
#                     print("inside none")
#                     raise Exception(f"Environment key: {MONGO_DB_URL} is not set.")
#                 MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile= ca)
#             self.client = MongoDBClient.client
#             self.database = self.client[database_name]
#         except Exception as e:
#             raise e
