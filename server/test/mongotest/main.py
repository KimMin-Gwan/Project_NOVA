from db import *
from data_domain import *

if __name__ == '__main__':
    test_db = DBTest()
    test_user = User()

    #test_db.ping_test()
    #콜렉션 리스트 설정 후 출력
    test_db.get_list_collection()
    print(test_db.collection_list)

    #콜렉션 선택
    test_db.set_collection(collection='user')

    #print(test_db.get_data_with_id(target='uid',id='8670-yfgh-5978'))

    print(test_db.get_all_data())

    #업로드
    #test_db.upload(document=test_user.get_dict_form_data())