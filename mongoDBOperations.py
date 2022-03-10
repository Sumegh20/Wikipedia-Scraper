import pymongo
import pandas as pd

class MongoDBManagement:
    def __init__(self, userid, password):
        try:
            self.userid = userid
            self.password = password
            self.url = "mongodb+srv://{}:{}@cluster0.xyxko.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(
                self.userid, self.password)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n" + str(e))

    def getMongoDBClientObject(self):
        try:
            client_object = pymongo.MongoClient(self.url)
            return client_object
        except Exception as e:
            raise Exception(f"(getMongoDBClientObject): Something went wrong in mongodb client object\n" + str(e))

    def isDatabasePresent(self,db_name):
        try:
            mongodb_client = self.getMongoDBClientObject()
            if db_name in mongodb_client.list_database_names():
                # print(f"{db_name} is present in mongodb")
                return True
            else:
                # print(f"{db_name} is not present in mongodb")
                return False
        except Exception as e:
            raise Exception(f"(isDatabasePresent): Something went wrong in isDatabasePresent\n" + str(e))

    def createDatabase(self, db_name):
        try:
            mongodb_client = self.getMongoDBClientObject()
            if self.isDatabasePresent(db_name=db_name):
                print(f"No need to create {db_name}")
            else:
                mongodb_database = mongodb_client[db_name]
                return mongodb_database
        except Exception as e:
            raise Exception(f"(createDatabase): Something went wrong on creating database\n" + str(e))

    def getDatabase(self, db_name):
        try:
            mongodb_client = self.getMongoDBClientObject()

            if self.isDatabasePresent(db_name=db_name):
                return mongodb_client[db_name]
            else:
                dataBase = self.createDatabase(db_name=db_name)
                return dataBase
        except Exception as e:
            raise Exception(f"(getDatabase): Something went wrong on getting database\n" + str(e))

    def isCollectionPresent(self, db_name, collection_name):
        try:
            if self.isDatabasePresent(db_name=db_name):
                database = self.getDatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    # print(f"{collection_name} is present in the {db_name}(database)")
                    return True
                else:
                    # print(f"{collection_name} is not present in the {db_name}(database)")
                    return False
            else:
                # print(f"The {collection_name}(collection) and {db_name}(database) both are not present")
                return False
        except Exception as e:
            raise Exception(f"(isCollectionPresent): Something went wrong in isCollectionPresent\n" + str(e))

    def createCollection(self, db_name, collection_name):
        try:
            if self.isCollectionPresent(db_name=db_name, collection_name=collection_name):
                print(f"No need to create collection {collection_name}")
            else:
                if self.isDatabasePresent(db_name=db_name):
                    database = self.getDatabase(db_name=db_name)
                    collection = database[collection_name]
                    return collection
                else:
                    database = self.createDatabase(db_name=db_name)
                    collection = database[collection_name]
                    return collection
        except Exception as e:
            raise Exception(f"(createCollection): Something went wrong on creating collection\n" + str(e))

    def getCollection(self, db_name, collection_name):
        try:
            if self.isCollectionPresent(db_name=db_name, collection_name=collection_name):
                database = self.getDatabase(db_name=db_name)
                collection = database[collection_name]
                return collection
            else:
                collection = self.createCollection(db_name=db_name, collection_name=collection_name)
                return collection
        except Exception as e:
            raise Exception(f"(getCollection): Something went wrong on getting collection\n" + str(e))

    def dropCollection(self, db_name, collection_name):
        try:
            if self.isCollectionPresent(db_name=db_name, collection_name=collection_name):
                collection = self.getCollection(db_name=db_name, collection_name=collection_name)
                collection.drop()
                print(f"{collection_name} is successfully drop from the {db_name}(database)")
                return True
            else:
                print(f"{collection_name} is not present in the {db_name}(database)")
                return False
        except Exception as e:
            raise Exception(f"(dropCollection): Something went wrong on deleting collection\n" + str(e))

    def insertOneRecord(self, record, db_name, collection_name):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            collection.insert_one(document=record)
            print(f"One record inserted in {collection_name}")
        except Exception as e:
            raise Exception(f"(insertOneRecord): Something went wrong on inserting one record\n" + str(e))

    def insertManyRecord(self, records, db_name, collection_name):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            collection.insert_many(document=records)
            print(f"Records inserted in {collection_name}")
        except Exception as e:
            raise Exception(f"(insertManyRecord): Something went wrong on inserting many record\n" + str(e))

    def getAllRecords(self, db_name, collection_name):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            result = collection.find()
            return result
        except Exception as e:
            raise Exception(f"(getAllRecords): Something went wrong on finding all record\n" + str(e))

    def getRecordsOnQuery(self, db_name, collection_name, query):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            result = collection.find(query)
            return result
        except Exception as e:
            raise Exception(f"(getRecordsOnQuery): Something went wrong on finding the record\n" + str(e))

    def updateRecords(self, db_name, collection_name, condition, update_data):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            collection.update_many(filter=condition, update=update_data)
            print("Successfully updated records according to the query")
        except Exception as e:
            raise Exception(f"(updateRecords): Something went wrong on updating the records\n" + str(e))

    def deleteRecord(self, db_name, collection_name, query):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            collection.delete_one(filter=query)
            print("Successfully deleted one record from collection")
        except Exception as e:
            raise Exception(f"(deleteRecord): Something went wrong on deleting a records\n" + str(e))

    def deleteManyRecordes(self, db_name, collection_name, query):
        try:
            collection = self.getCollection(db_name=db_name, collection_name=collection_name)
            collection.delete_many(filter=query)
            print("Successfully deleted one record from collection")
        except Exception as e:
            raise Exception(f"(deleteRecord): Something went wrong on deleting a records\n" + str(e))

    def getDataFrameOfCollection(self, db_name, collection_name, query):
        try:
            all_Records = self.getRecordsOnQuery(collection_name=collection_name, db_name=db_name, query=query)
            dataframe = pd.DataFrame(all_Records)
            return dataframe
        except Exception as e:
            raise Exception(
                f"(getDataFrameOfCollection): Failed to get DatFrame from provided collection and database.\n" + str(e))

    def getResultToDisplayOnBrowser(self, db_name, collection_name, query):
        try:
            response = self.getRecordsOnQuery(db_name=db_name, collection_name=collection_name, query=query)
            result = [i for i in response]
            return result
        except Exception as e:
            raise Exception(
                f"(getResultToDisplayOnBrowser) - Something went wrong on getting result from database.\n" + str(e))
