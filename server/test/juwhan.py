import requests

import os
import json
from pprint import pprint


def try_add_user_test():
    with open('./test_user.json', 'r', encoding='utf-8') as f:
        user_dict = json.load(f)

    #pprint(user_dict)

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    print(f"현재 파일 디렉토리: {script_dir}")
    test_user_path = script_dir + "/test_user.json"

    params = {
        'user_data_url': test_user_path,
    }

    result = requests.get(url="http://127.0.0.1:6000/testing/try_add_user",params=params)
    print(result)

def try_delete_user_test():
    params = {
        'target_uid' : 'asd0-19xd-a223'
    }
    result = requests.get(url="http://127.0.0.1:6000/testing/try_remove_user",params=params)
    print(result)

def try_add_feed_test():
    with open('./test_feed.json', 'r', encoding='utf-8') as f:
        feed_dict = json.load(f)

    #pprint(user_dict)

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    print(f"현재 파일 디렉토리: {script_dir}")
    test_feed_path = script_dir + "/test_feed.json"

    params = {
        'feed_data_url': test_feed_path,
    }
    result = requests.get(url="http://127.0.0.1:6000/testing/try_add_feed",params=params)
    print(result)

def try_delete_feed_test():
    params = {
        'target_fid' : '34'
    }

    result = requests.get(url="http://127.0.0.1:6000/testing/try_remove_feed",params=params)
    print(result)

def try_like_feed():
    params = {
        'fid' : '5',
        'uid' : "abcd-1234-5678"
    }

    result = requests.get(url="http://127.0.0.1:6000/testing/try_like_feed",params=params)
    print(result)

def try_dislike_feed():
    params = {
        'fid' : '5',
        'uid' : "abcd-1234-5678"
    }

    result = requests.get(url="http://127.0.0.1:6000/testing/try_dislike_feed",params=params)
    print(result)

# try_add_user_test()
# try_delete_user_test()
# try_add_feed_test()
# try_delete_feed_test()
# try_like_feed()
# try_dislike_feed()