import json

def main():
    data_list = []
    dict_data = {
        "9999" : 0,
        "9998" : 0,
        "9997" : 0,
        "9996" : 0,
        "9995" : 0,
        "9994" : 0,
        "9993" : 0,
        "9992" : 0,
    }

    new_data = []

    with open("./../src/model/local_database/user.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))

        #for bid in dict_data.keys():
            #for data in data_list:
                #if data['group_bid'] == bid:
                    #dict_data[bid] += 1

        #print(dict_data)

        for data in data_list:
            sample = {'muid' : data['uid'],
                      'option' : [],
                      'history' : []
                      }

            new_data.append(sample)

    with open("./../src/model/local_database/managed_user.json", 'w',  encoding='utf-8' )as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


main()