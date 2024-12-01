from copy import copy

# 리스트를 이용한 포인터

data = [1]  # 포인터

def func1(sample):
    data = copy(sample)
    data[0] = 2
    print(data)




from bintrees import AVLTree



# 객체를 이용한 포인터

tree = AVLTree()

class Edge:
        self.__user_node_avltree
    def __init__(self):
        self.

class UserNode:
    def __init__(self):
        self.age=1
        self.edge = []
        

user = UserNode()


tree.insert(key=1, value=user)
table.append(user)

print(tree.get(1))
print(table[0])







feed_algo.add_feed()


class FeedAlgo:
    def __init__(self, database):
        self.graph
        self.feed_node_avltree = AVLTree()
        self.user_node_avltree = AVLTree()
        self.hash_node_avltree = AVLTree()
        self.__init_graph(database=database)
        self.graph()


    def __init_graph(self, database):
        user_datas = database.get_all_data(target_id="uid")
        user_list = []

        for user_data in user_datas:
            user = User()
            user.make_with_dict(user_data)
            user_list.append(user)

        for single_user in user_list:
            self.add_user_node(uid=single_user.uid)

        feed_datas = database.get_all_data(target_id="fid")
        feed_list = []

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feed_list.append(user)

        for single_feed in feed_list:
            self.add_feed_node(feed=single_feed)

        return

    def modify_user_node(self, user:User):
        user_node = self.user_node_avltree.get(uid)
        feed_node_list = []

        for like_id in user.like:
            # 스프릿할것
            fid = "fid"
            date = "date"
            # date를 datetime 객체로 바꿀것 

            feed_node = self.feed_node_avltree.get(fid)

            # 이미 커넥트 되어있다면 안해도됨
            self.graph.connect_user_with_feed(feed_node, user_node, date=date)

            feed_node_list.append(feed_node)

        # 근데 리스트에 없는데 연결된 피드가 있음<
        # 그럼 그 연결을 지우는 절차가 있어야됨
        self.graph.clear_user_node_with_edge(user_node, feed_node_list)


        return


    def add_feed_node(self, feed:Feed):
        feed_node = self.graph.add_feed_node(feed.fid, feed.date)

        # hash_node가 이미 존재하는가? -> 그래프 안에 있어야됨(add_hash_node 함수 안에 있어야됨)
        hash_nodes = self.graph.add_hash_node(feed_node, feed.hashtag, feed.date)


        self.graph.connect_feed_with_hash(feed_node, hash_nodes, feed.date)
        self.feed_node_avltree.insert(key=fid, value = feed_node)

        for hash_node in hash_nodes:
            self.hash_node_avltree.insert(key=hash_node.hashtag, value = hash_node)

        user_node = self.user_node_avltree.get(feed.uid)

        self.graph.connect_user_with_feed(feed_node, user_node, date=feed.date)
        return True

    def add_user_node(self, uid):
        user_node = self.graph.add_user_node(uid)
        self.user_node_avltree.inster(key=uid, value= user_node)

    def modify_feed_node(self, feed):
        feed_node = self.feed_node_avltree.get(key=feed.fid)


    def recommand_next_feed(self, feed:Feed, history:list):
        # 1. 유저와 피드 간의 관계
        # 2. 해시태그와 피드 간의 관계

        # 3. 결과 값 리턴 (fid 리스트가 올것)

        result_fid_list = []

        for fid in result_fid_list:
            if fid not in history:
                return fid

        return None

from pprint import pprint

class CGraph:
    def __init__(self):
        self.num_feed_node = 0
        self.num_hash_node = 0
        self.num_user_node = 0

    def __call__(self):
        print(f'INFO<-[      {num_feed} NOVA Graph IN SEARCH ENGINE NOW READY.')


    def __is_hash_node_exist(self, hashtag, tree) -> bool:
        if tree.get(hashtag):
            return
