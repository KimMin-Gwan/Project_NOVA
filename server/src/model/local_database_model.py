import json
from others import DatabaseLogicError
from copy import copy

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pprint import pprint

class Local_Database:
    def __init__(self) -> None:
        self.__db_file_path = './model/local_database/'
        self.__data_files = {
            'banner_file' : 'banner.json',
            'bias_file' : 'bias.json',
            'feed_file' : 'feed.json',
            'user_file' : 'user.json',
            'comment_file' : 'comment.json',
            'alert_file' : 'alert.json',
            'notice_file' : 'notice.json',
            'project_file' : 'project.json',
            'interaction_file' : 'interaction.json',
            'feed_link_file' : 'feed_link.json',
            'report_file' : 'report.json'
        }
        self.__read_json()

    def __read_json(self):
        self.__banner_data = []
        self.__bias_data = []
        self.__feed_data = []
        self.__user_data = []
        self.__comment_data = []
        self.__alert_data = []
        self.__notice_data = []
        self.__project_data = []
        self.__interaction_data= []
        self.__feed_link_data = []
        self.__report_data = []


        data_list = [self.__banner_data, self.__bias_data, self.__feed_data, self.__user_data,
                     self.__comment_data, self.__alert_data, self.__notice_data,
                    self.__project_data, self.__interaction_data, self.__feed_link_data, self.__report_data]

        for file_name, list_data in zip(self.__data_files.values(), data_list):
            with open(self.__db_file_path+file_name, 'r',  encoding='utf-8' )as f:
                list_data.extend(json.load(f))


    def __save_json(self, file_name, data):
        path = self.__db_file_path
        with open(path+file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return

    # 저장하기
    def __save_feed_json(self):
        file_name = self.__data_files['feed_file']
        self.__save_json(file_name, self.__feed_data)
        return

    # 저장하기
    def __save_user_json(self):
        file_name = self.__data_files['user_file']
        self.__save_json(file_name, self.__user_data)
        return

    # 저장하기
    def __save_banner_json(self):
        file_name = self.__data_files['banner_file']
        self.__save_json(file_name, self.__banner_data)
        return

    # 저장하기
    def __save_bias_json(self):
        file_name = self.__data_files['bias_file']
        self.__save_json(file_name, self.__bias_data)
        return


    # 저장하기
    def __save_comment_json(self):
        file_name = self.__data_files['comment_file']
        self.__save_json(file_name, self.__comment_data)
        return

    # 저장하기
    def __save_alert_json(self):
        file_name = self.__data_files['alert_file']
        self.__save_json(file_name, self.__alert_data)
        return

    # 저장하기
    def __save_notice_json(self):
        file_name = self.__data_files['notice_file']
        self.__save_json(file_name, self.__notice_data)
        return

    # 저장하기
    def __save_project_json(self):
        file_name = self.__data_files['project_file']
        self.__save_json(file_name, self.__project_data)
        return

    # 저장하기
    def __save_interaction_json(self):
        file_name = self.__data_files['interaction_file']
        self.__save_json(file_name, self.__interaction_data)
        return
    
    # 저장하기
    def __save_feed_link_json(self):
        file_name = self.__data_files['feed_link_file']
        self.__save_json(file_name, self.__feed_link_data)
        return
    
    # 저장하기
    def __save_report_json(self):
        file_name = self.__data_files['report_file']
        self.__save_json(file_name, self.__report_data)
        return

    # db.get_data_with_key(target="user", key="uname", key_data="minsu")
    def get_data_with_key(self, target:str, key:str, key_data:str):
        try:
            list_data = self._select_target_list(target=target)
            find_data = None
            for data in list_data:
                if data[key] == key_data:
                    find_data = data
            return find_data
        except Exception as e:
            raise DatabaseLogicError("get_data_with_key error | " + str(e))

    # db.get_datas_with_key(target="user", key="uname", key_datas=["minsu", "minzi"])
    def get_datas_with_key(self, target:str, key:str, key_datas:list):
        try:
            list_data = self._select_target_list(target=target)
            find_datas = []
            for key_data in key_datas:
                for data in list_data:
                    if key_data == data[key]:
                        find_datas.append(data)
            return find_datas
        except Exception as e:
            raise DatabaseLogicError("get_datas_with_key error | " + str(e))
        

    # db.get_data_with_id(target="uid", id="1001")
    def get_data_with_id(self, target:str, id:str):
        try:
            list_data = self._select_target_list(target=target)
            find_data = None
            for data in list_data:
                if data[target] == id:
                    find_data = data
            return find_data
        except Exception as e:
            raise DatabaseLogicError("get_data_with_id error | " + str(e))

    # db.get_datas_with_ids(target="uid", ids=["1001", "1002"])
    def get_datas_with_ids(self, target_id:str, ids:list):
        try:
            list_data = self._select_target_list(target=target_id)
            find_datas = []
            for id in ids:
                for data in list_data:
                    if id == data[target_id]:
                        find_datas.append(data)
            return find_datas
        except Exception as e:
            raise DatabaseLogicError("get_datas_with_ids error | " + str(e))

    def get_all_data(self, target):
        return self._select_target_list(target=target)
    

    def _select_target_list(self, target:str):
        if target == "baid" or target == "banner":
            return self.__banner_data
        elif target == "bid" or target == "bias":
            return self.__bias_data
        elif target == "fid" or target == "feed":
            return self.__feed_data
        elif target == "uid" or target == "user":
            return self.__user_data
        elif target == "cid" or target == "comment":
            return self.__comment_data
        elif target == "aid" or target == "alert":
            return self.__alert_data
        elif target == "nid" or target == "notice":
            return self.__notice_data
        elif target == "pid" or target == "project":
            return self.__project_data
        elif target == "iid" or target == "interaction":
            return self.__interaction_data
        elif target == "lid" or target == "feed_link":
            return self.__feed_link_data
        elif target == "rid" or target == "report":
            return self.__report_data
        else:
            raise DatabaseLogicError("target id did not define")
        
    # db.modify_data_with_id(target="uid", target_data={key: value})
    def modify_data_with_id(self, target_id, target_data:dict):
        try:
            target_index = -1
            target_list = self._select_target_list(target=target_id)

            for i, data in enumerate(target_list):
                if data[target_id] == target_data[target_id]:
                    target_index = i
                    break
                i+=1

            if target_index == -1:
                return False
            
            target_list[target_index] = target_data
            func = self._select_save_function(target=target_id)
            func()
            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="modifiy_data_with_id error | " + str(e))

    # db.add_new_data(target_id="uid", new_data={key: value})
    def add_new_data(self, target_id:str, new_data:dict):
        try:
            target_list:list = self._select_target_list(target=target_id)
            target_list.append(new_data)
            func = self._select_save_function(target=target_id)
            func()
        except Exception as e:
            raise DatabaseLogicError("add_new_data error | " + str(e))
        return True
    
    # 한번에 여러 데이터 인풋
    # db.add_new_data(target_id="uid", new_data=[{key: value}])
    def add_new_datas(self, target_id:str, new_datas:list):
        try:
            target_list:list = self._select_target_list(target=target_id)
            for new_data in new_datas:
                target_list.append(new_data)
            func = self._select_save_function(target=target_id)
            func()
        except Exception as e:
            raise DatabaseLogicError("add_new_data error | " + str(e))
        return True
    
    def _select_save_function(self, target:str):
        if target == "baid" or target == "banner":
            return self.__save_banner_json
        elif target == "bid" or target == "bias":
            return self.__save_bias_json
        elif target == "fid" or target == "feed":
            return self.__save_feed_json
        elif target == "uid" or target == "user":
            return self.__save_user_json
        elif target == "cid" or target == "comment":
            return self.__save_comment_json
        elif target == "aid" or target == "alert":
            return self.__save_alert_json
        elif target == "nid" or target == "notice":
            return self.__save_notice_json
        elif target == "pid" or target == "project":
            return self.__save_project_json
        elif target == "iid" or target == "interaction":
            return self.__save_interaction_json
        elif target == "lid" or target == "feed_link":
            return self.__save_feed_link_json
        elif target == "rid" or target == "report":
            return self.__save_report_json
        else:
            raise DatabaseLogicError("target id did not define")

    # db.get_num_list_with_id(target_id="uid")
    def get_num_list_with_id(self, target_id:str):
        target_list:list = self._select_target_list(target=target_id)
        num_list= len(target_list)
        return num_list
    
    #데이터 삭제
    def delete_data_with_id(self,target:str, id:str):
        try:
            target_index = -1
    
            target_list = self._select_target_list(target=target)

            for i, data in enumerate(target_list):
                if data[target] == id:
                    target_index = i
                    break
                i+=1

            if target_index == -1:
                return False
            
            target_list.pop(target_index)
            func = self._select_save_function(target=target)
            func()
            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="delete_data_with_id error | " + str(e))

    #데이터 한번에 여러개 삭제
    def delete_datas_with_ids(self,target:str, ids:str):
        try:
            target_indexes = []
    
            target_list = self._select_target_list(target=target)

            for i, data in enumerate(target_list):
                if data[target] in ids:
                    target_indexes.append(i)

                if len(ids) == len(target_indexes):
                    break

            # 요청한 삭제 데이터 길이랑 찾은 데이터 길이가 다르면 지우지 말고 걍 실패
            if len(ids) != len(target_indexes):
                return False
            
            for index in target_indexes:
                target_list.pop(index)

            func = self._select_save_function(target=target)
            func()
            return True

        except Exception as e:
            print(e)
            raise DatabaseLogicError(error_type="delete_data_with_id error | " + str(e))
    

# 실제로 사용할 몽고 디비
class Mongo_Database(Local_Database):
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
        collection.insert_many(document=document)
        return

    #(찾기)
    def __find_one(self,document, collection:Collection) -> None:
        return collection.find_one(document,{'_id':False})
    
    def __find_many(self,document, collection:Collection) -> None:
        return list(collection.find({"$or" : document},{'_id':False}))
    
    #수정
    def __update_one(self,document,data , collection:Collection) -> None:
        collection.update_one(document,{'$set':data})
        return
    #삭제
    def __delete_one(self,document, collection:Collection) -> None:
        collection.delete_one(document=document)
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
            raise DatabaseLogicError("get_data_with_key error | " + str(e))

    # db.get_datas_with_key(target="user", key="uname", key_datas=["minsu", "minzi"])
    def get_datas_with_key(self, target:str, key:str, key_datas:list):
        try:
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)
            find_datas = []
            for key_data in key_datas:
                find_datas.append(self.__find_one({f'{key}':f'{key_data}'}, collection=selected_collection))

            return find_datas
        except Exception as e:
            raise DatabaseLogicError("get_datas_with_key error | " + str(e))
        

    # db.get_data_with_id(target="uid", id="1001")
    def get_data_with_id(self, target:str, id:str):
        try:
            collection_name = self._select_target_list(target=target)
            selected_collection = self.__set_collection(collection=collection_name)
            
            find_data = self.__find_one({f'{target}':f'{id}'},collection=selected_collection)

            return find_data
        except Exception as e:
            raise DatabaseLogicError("get_data_with_id error | " + str(e))

    # db.get_datas_with_ids(target="uid", ids=["1001", "1002"])
    def get_datas_with_ids(self, target_id:str, ids:list):
        try:
            collection_name = self._select_target_list(target=target_id)
            selected_collection = self.__set_collection(collection=collection_name)
            datas = []
            for id in ids:
                datas.append({f'{target_id}' : f'{id}'})
            
            #append(self.__find_one({f'{target_id}':f'{id}'},collection=selected_collection))
            find_datas = self.__find_many(document=datas, collection=selected_collection)

            return find_datas
        except Exception as e:
            raise DatabaseLogicError("get_datas_with_ids error | " + str(e))

    def get_all_data(self, target):
        collection_name = self._select_target_list(target=target)
        selected_collection = self.__set_collection(collection=collection_name)
        find_data = self.__find_many(document={},collection=selected_collection)
        #return list(selected_collection.find({},{'_id':False}))
        return find_data
    
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
    
