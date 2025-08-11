from others import DatabaseLogicError
from pymongo import UpdateOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pprint import pprint


# 실제로 사용할 몽고 디비
class Mongo_Database():
    def __init__(self, uri) -> None:
        #MongoDB연결 uri
        # Create a new client and connect to the server
        self.__client = MongoClient(uri, server_api=ServerApi('1'))
        self.__db = self.__client.NovaDB    #사용 할 때 DB이름에 맞게 변경 필요
        self.collection_list = []

    def __set_collection(self,collection) -> None:
        return self.__db[f'{collection}']

    #저장(업로드)
    def __upload_one(self,document, collection:Collection) -> None:
        collection.insert_one(document=document)
        return
    #업로드(업로드 여러개)
    def __upload_many(self,document, collection:Collection) -> None:
        collection.insert_many(documents=document)
        return

    #(찾기)
    def __find_one(self,document, collection:Collection) -> None:
        return collection.find_one(document,{'_id':False})
    
    def __find_many(self,document, collection:Collection) -> None:
        return list(collection.find({"$or" : document},{'_id':False}))
    
    #수정
    def __update_one(self,document, data, collection:Collection) -> None:
        collection.update_one(document,{'$set':data})
        return
    
    def __bulk_update(self,target_id:str, ids:list, datas: list[dict], collection: Collection) -> None:
        # Bulk write 작업을 위한 리스트 준비
        bulk_operations = []
    
        for filter_, update_data in zip(ids, datas):
            
            if filter_ and update_data:
                # UpdateOne 작업 생성
                bulk_update_one = UpdateOne({f"{target_id}" : filter_}, {"$set": update_data})
                bulk_operations.append(bulk_update_one)
    
        # 한 번에 bulk_write로 업데이트 수행
        if bulk_operations:
            collection.bulk_write(bulk_operations)
        return
    
    #삭제
    def __delete_one(self, document, collection:Collection) -> None:
        collection.delete_one(document)
        return

    # def __save_json(self, file_name, data):
    #     collection = self.__set_collection(collection=file_name)
    #     self.__upload_one(document=data, collection=collection)
    #     return

    def get_data_with_key(self, target:str, key:str, key_data:str):
        try:
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)
            find_data = self.__find_one({f'{key}':f'{key_data}'}, collection=selected_collection)

            return find_data
        except Exception as e:
            print(e)
            raise

    # db.get_datas_with_key(target="user", key="uname", key_datas=["minsu", "minzi"])
    def get_datas_with_key(self, target:str, key:str, key_datas:list):
        try:
            find_datas = []
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)
            #find_datas = []
            #for key_data in key_datas:
            #    find_datas.append(self.__find_one({f'{key}':f'{key_data}'}, collection=selected_collection))

            datas = []
            for key_data in key_datas:
                datas.append({f'{key}' : f'{key_data}'})
            
            #append(self.__find_one({f'{target_id}':f'{id}'},collection=selected_collection))
            if datas:
                find_datas = self.__find_many(document=datas, collection=selected_collection)

            return find_datas
        except Exception as e:
            print(e)
            raise
        

    # db.get_data_with_id(target="uid", id="1001")
    def get_data_with_id(self, target:str, id:str):
        try:
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)
            
            find_data = self.__find_one({f'{target}':f'{id}'},collection=selected_collection)

            return find_data
        except Exception as e:
            print(e)
            raise

    # db.get_datas_with_ids(target="uid", ids=["1001", "1002"])
    def get_datas_with_ids(self, target_id:str, ids:list):
        try:
            find_datas = []
            collection_name = self._select_target_list(target=target_id)
            selected_collection = self.__set_collection(collection=collection_name)
            datas = []
            for id in ids:
                datas.append({f'{target_id}' : f'{id}'})
            
            #append(self.__find_one({f'{target_id}':f'{id}'},collection=selected_collection))
            
            if datas:
                find_datas = self.__find_many(document=datas, collection=selected_collection)

            return find_datas
        except Exception as e:
            print(e)
            raise

    def get_all_data(self, target):
        collection_name = self._select_target_list(target=target)
        selected_collection = self.__set_collection(collection=collection_name)
        #find_data = self.__find_many(document=[{}],collection=selected_collection)
        return list(selected_collection.find({},{'_id':False}))
        #return find_data
    
    def _select_target_list(self, target:str):
        if target == "baid" or target == "banner":
            return "banner"
        elif target == "bid" or target == "bias":
            return "bias"
        elif target == "fid" or target == "feed":
            return "feed"
        elif target == "uid" or target == "user":
            return "user"
        elif target == "cid" or target == "comment":
            return "comment"
        elif target == "aid" or target == "alert":
            return "alert"
        elif target == "nid" or target == "notice":
            return "notice"
        elif target == "pid" or target == "project":
            return "project"
        elif target == "iid" or target == "interaction":
            return "interaction"
        elif target == "lid" or target == "feed_link":
            return "feed_link"
        elif target == "rid" or target == "report":
            return "report"
        elif target == "tuid" or target == "time_table_user":
            return "time_table_user"
        elif target == "seid" or target == "schedule_event":
            return "schedule_event"
        elif target == "sbid" or target == "schedule_bundle":
            return "schedule_bundle"
        elif target == "sid" or target == "schedule":
            return "schedule"
        elif target == "duid" or target == "deleted_user":
            return "deleted_user"
        elif target == "content_id" or target == "content":
            return "content"
        else:
            raise DatabaseLogicError("target id did not define")
        
    # db.modify_data_with_id(target="uid", target_data={key: value})
    def modify_data_with_id(self, target_id, target_data:dict):
        try:
            collection_name = self._select_target_list(target=target_id)
            selected_collection = self.__set_collection(collection=collection_name)
            
            self.__update_one({f'{target_id}':f'{target_data[target_id]}'},data=target_data,collection=selected_collection)
            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="modifiy_data_with_id error | " + str(e))

    # 반드시 ids와 target_datas는 동일한 순서로 같은 갯수가 와야됨
    def modify_datas_with_ids(self, target_id, ids:list, target_datas:list):
        try:
            collection_name = self._select_target_list(target=target_id)
            selected_collection = self.__set_collection(collection=collection_name)
            
            self.__bulk_update(target_id=target_id, ids=ids, datas=target_datas, collection=selected_collection)
            #self.__update_one({f'{target_id}':f'{target_data[target_id]}'},data=target_data,collection=selected_collection)
            
            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="modifiy_data_with_id error | " + str(e))

    def add_new_data(self, target_id:str, new_data:dict):
        try:
            collection_name = self._select_target_list(target=target_id)
            selected_collection = self.__set_collection(collection=collection_name)
            
            # document요? 그건 뭐지? 어디다 넣죠? new_data가 어디로 가야됨
            self.__upload_one(document=new_data, collection=selected_collection)

        except Exception as e:
            raise DatabaseLogicError("add_new_data error | " + str(e))
        return True
    
    # db.add_new_data(target_id="uid", new_data=[{key: value}])
    def add_new_datas(self, target_id:str, new_datas:list):
        try:
            collection_name = self._select_target_list(target=target_id)
            selected_collection = self.__set_collection(collection=collection_name)

            self.__upload_many(document=new_datas, collection=selected_collection)

        except Exception as e:
            raise DatabaseLogicError("add_new_data error | " + str(e))
        return True

    def get_num_list_with_id(self, target_id:str):
        collection_name = self._select_target_list(target=target_id)
        selected_collection = self.__set_collection(collection=collection_name)
        num_list= len(list(selected_collection.find({},{'_id':False})))
        return num_list
    
    #데이터 삭제
    def delete_data_with_id(self,target:str, id:str):
        try:
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)
            self.__delete_one(document={f'{target}':f'{id}'},collection=selected_collection)

            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="delete_data_with_id error | " + str(e))

    #데이터 한번에 여러개 삭제
    def delete_datas_with_ids(self,target:str, ids:str):
        try:
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)

            for id in ids:
                self.__delete_one(document={f'{target}':f'{id}'},collection=selected_collection)

            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="delete_data_with_id error | " + str(e))
    
