import json

def main():
    data_list = []
    dict_data = {
        "1001" : 0,
        "1002" : 0,
        "1003" : 0,
        "1004" : 0,
        "1005" : 0,
        "1006" : 0,
        "1007" : 0,
        "1008" : 0,
        "1009" : 0,
        "1010" : 0,
        "1011" : 0,
        "1012" : 0,
        "1013" : 0,
        "1014" : 0,
        "1015" : 0,
        "1016" : 0,
        "1017" : 0,
    }



    with open("./../src/model/local_database/user.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))

    for key in dict_data.keys():
        for data in data_list:
            if data['solo_bid'] == key:
                dict_data[key] += 1

    print(dict_data)


main()