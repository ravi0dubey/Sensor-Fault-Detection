from sensor.configuration.mongo_db_connection import   MongoDBClient
if __name__=='__main__':
    mongodb_client = MongoDBClient()
    # print(mongodb_client.database)
    # print("collection names: " ,mongodb_client)
    # print(mongodb_client.database)
    print("collection names: " ,mongodb_client.database.list_collection_names())

    
    