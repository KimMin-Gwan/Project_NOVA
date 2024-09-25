import json
from others import DatabaseLogicError


class Local_Database:
    def __init__(self) -> None:
        self.__db_file_path = './model/local_database/'
        self.__data_files = {
            'banner_file' : 'banner.json',
            'bias_file' : 'bias.json',
            'feed_file' : 'feed.json',
            'league_file' : 'league.json',
            'name_card_file' : 'name_card.json',
            'user_file' : 'user.json',
            'managed_user_file' : 'managed_user.json',
            'comment_file' : 'comment.json'
        }
        self.__read_json()

    def __read_json(self):
        self.__banner_data = []
        self.__bias_data = []
        self.__feed_data = []
        self.__league_data = []
        self.__name_card_data = []
        self.__user_data = []
        self.__managed_user_data = []
        self.__comment_data = []

        data_list = [self.__banner_data, self.__bias_data, self.__feed_data,
                      self.__league_data, self.__name_card_data, self.__user_data,
                      self.__managed_user_data, self.__comment_data ]

        for file_name, list_data in zip(self.__data_files.values(), data_list):
            with open(self.__db_file_path+file_name, 'r',  encoding='utf-8' )as f:
                list_data.extend(json.load(f))


    def __save_json(self, file_name, data):
        path = self.__db_file_path
        with open(path+file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return

    # 저장하기
    def __save_name_card_json(self):
        file_name = self.__data_files['name_card_file']
        self.__save_json(file_name, self.__name_card_data)
        return

    # 저장하기
    def __save_league_json(self):
        file_name = self.__data_files['league_file']
        self.__save_json(file_name, self.__league_data)
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
    def __save_managed_user_json(self):
        file_name = self.__data_files['managed_user_file']
        self.__save_json(file_name, self.__managed_user_data)
        return

    # 저장하기
    def __save_comment_json(self):
        file_name = self.__data_files['comment_file']
        self.__save_json(file_name, self.__comment_data)
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
        elif target == "lid" or target == "league":
            return self.__league_data
        elif target == "ncid" or target == "name_card":
            return self.__name_card_data
        elif target == "uid" or target == "user":
            return self.__user_data
        elif target == "muid" or target == "managed_user":
            return self.__managed_user_data
        elif target == "cid" or target == "comment":
            return self.__comment_data
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

    def _select_save_function(self, target:str):
        if target == "baid" or target == "banner":
            return self.__save_banner_json
        elif target == "bid" or target == "bias":
            return self.__save_bias_json
        elif target == "fid" or target == "feed":
            return self.__save_feed_json
        elif target == "lid" or target == "league":
            return self.__save_league_json
        elif target == "ncid" or target == "name_card":
            return self.__save_name_card_json
        elif target == "uid" or target == "user":
            return self.__save_user_json
        elif target == "muid" or target == "managed_user":
            return self.__save_managed_user_json
        elif target == "cid" or target == "comment":
            return self.__save_comment_json
        else:
            raise DatabaseLogicError("target id did not define")

    # db.get_num_list_with_id(target_id="uid")
    def get_num_list_with_id(self, target_id:str):
        target_list:list = self._select_target_list(target=target_id)
        num_list= len(target_list)
        return num_list
    
    #데이터 삭제
    def delete_data_With_id(self,target:str, id:str):
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
    
