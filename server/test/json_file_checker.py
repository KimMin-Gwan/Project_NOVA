import json

def main():
    data_list = []
    dict_data = {
    }

    new_data = []

    with open("./../src/model/local_database/feed.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))


        for data in data_list:
            data['hashtag'] = ["임시", "가짜해시태그"]
            new_data.append(data)

    with open("./../src/model/local_database/feed.json", 'w',  encoding='utf-8' )as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


main()