
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DBTest:
    def __init__(self) -> None:
        self.__uri = "mongodb+srv://admin:nova-db-password-43te7wuhbgi8we@nova-cluster.kz63a.mongodb.net/?retryWrites=true&w=majority&appName=Nova-Cluster"

        # Create a new client and connect to the server
        self.__client = MongoClient(self.__uri, server_api=ServerApi('1'))
        self.__db = self.__client.NovaDB
        self.collection_list = []
        self.__collection = None

    def ping_test(self):
        # Send a ping to confirm a successful connection
        try:
            self.__client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def set_collection(self,collection) -> None:
        self.__collection = self.__db[f'{collection}']
        return
    
    def upload(self,document) -> None:
        self.__collection.insert_one(document=document)

    def get_all_data(self):
        return list(self.__collection.find({},{'_id':False}))
    
    def __find_one(self,document) -> None:
        return self.__collection.find_one(document,{'_id':False})
        #return document
    
    def get_data_with_id(self, target:str, id:str):
        try:
            #list_data = self._select_target_list(target=target)
            find_data = self.__find_one({f'{target}':f'{id}'})
            # for data in list_data:
            #     if data[target] == id:
            #         find_data = data
            return find_data
        except Exception as e:
            raise e
    
    def get_list_collection(self):
        self.collection_list = self.__db.list_collection_names()