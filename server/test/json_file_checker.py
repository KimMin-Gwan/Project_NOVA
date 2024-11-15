import json
from pprint import pprint

def main():
    data_list = []
    #dict_data = {
        #"uid" : "",
        #"uname" : "",
        #"age" : "",
        #"email" : "",
        #"gender" : "m",
        #"credit" : 0,
        #"solo_bid" : "",
        #"group_bid" : "",
        #"password" : "sample122",
        #"alert" : [],
        #"like" : [],
        #"my_feed" : [],
        #"my_comment" : [],
        #"active_feed" : []
    #}

    new_data = []

    with open("./../src/model/local_database/user.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))

        pprint(data_list)
        




        #for data in data_list:
            #dict_data={}

            #dict_data['uid'] = data["uid"]
            #dict_data['uname'] = data["uname"]
            #dict_data['age'] = data["age"]
            #dict_data['email'] = data["email"]
            #dict_data['gender'] = data["gender"]
            #dict_data['credit'] = 0
            #dict_data['solo_bid'] = data['solo_bid']
            #dict_data['group_bid'] = data['group_bid']
            #dict_data['password'] = data['password']
            #dict_data['alert'] = []
            #dict_data['like'] = []
            #dict_data["my_comment"] = []
            #dict_data["active_feed"] = []
            #dict_data["feed_history"] = []
            #dict_data["my_feed"] = []
            #dict_data["feed_search_history"] = []

            #new_data.append(dict_data)

    #with open("./../src/model/local_database/user.json", 'w',  encoding='utf-8' )as f:
        #json.dump(new_data, f, ensure_ascii=False, indent=4)


main()