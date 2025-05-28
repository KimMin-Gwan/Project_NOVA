import random
from datetime import  datetime, timedelta
from pprint import pprint
from bintrees import AVLTree
from others.data_domain import Feed, User, Bias, Notice, Comment
# --------------------------------------------------------------------------------------------
YELLOW = "\033[33m"
RESET = "\033[0m"
# Edge 수도코드
# class Edge
#   __init__(target_node, gen_time:datetime):
#       self.target_node = target_node
#       self.get_time = gen_time        # 생성된 시간
#
#   equal(other) 오버로딩
#       조건: target_node와 Edge안에 있는 Target_node가 일치하는지 확인
#   sorted(other)
#       조건: generated time이 가장 최신순인 것이 먼저 오도록 하게 함
#           이 때, 값비교 시 timedelta값이 더 큰 쪽이 최신의 것이 됨.
#   weight():
#       시간차를 계산하는 함수
#   __calculate_timestamp():
#       current_time = datetime.now()
#       gen_time = datetime 객체로 만들어진 gen_time_str
#       return (current_time - gen_time).total_second()
#
#   get_target_node():
#       return target_node
#

# 노드 엣지 클래스
class Edge:
    def __init__(self, target_node, gen_time):
        self.target_node = target_node # 타겟 노드 저장
        self.gen_time:datetime = gen_time # 엣지의 생성 시간

        # 이 엣지는 Feed-User 의 경우, 좋아요(star)를 누른 시간, Feed를 작성한 시간을 가지게 됨
        # Feed-Hashtag 의 경우, Feed 생성 시간을 이어 받게됨.

    # 동일한 엣지인지 서로 비교 해야함.
    # 만약 향하는 노드가 같다면
    def __eq__(self, other):
        return self.target_node == other.target_node

    # 날짜가 더 최신의 edge 순으로 정렬
    def __lt__(self, other):
        return self.gen_time > other.gen_time

    # 출력 포맷
    def __str__(self):
        return 'Edge({}, {})'.format(self.target_node.get_id(), self.gen_time)

    # edge 리스트 출력 포맷
    def __repr__(self):
        return 'Edge({}, {})'.format(self.target_node.get_id(), self.gen_time)

    # 내부함수로 구현함. 초 단위로 계산함
    def weight(self):
        return self.__calculate_timestamp()

    # 향하고 있는 타겟 노드 얻기
    def get_target_node(self):
        return self.target_node

    # 내부 함수로 정의된 가중치 부여 함수 (매업데이트 되는것보다 제때 구하는 걸로)
    def __calculate_timestamp(self):
        # 왜인지는 모르겠지만, 현재 시간을 포맷에 맞게 변환하는데, datetime → str → datetime으로 변환해야 함.
        current_time_str = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        current_time = datetime.strptime(current_time_str, "%Y/%m/%d-%H:%M:%S")

        # datetime 연산 시 timedelta값 반환
        time_difference = current_time - self.gen_time
        return time_difference.total_seconds() # timedelta 값을 초 단위로 변환하여 제공

# BaseNode 수도코드
# class BaseNoe
#     initalize_varialbes
#           edges = {}      # 필요한 엣지를 담음
#           node_type 노드 타입 : 노드의 타입을 정의함. 엣지를 담을 때, 공통된 노드만을 담게하기 위해서 넣음
#
#   공통된 함수들 중, 추가, 삭제, 엣지 찾기를 내부함수로 구현
#     1. __add_edge(target_node, gen_time):
#         node_type = target_node.node_type
#         edge = Edge(target_node, gen_time)  # 엣지 생성
#         edges[node_type].append(edge)
#
#     2. __remove_edge(target_node):
#         node_type = target_node.node_type
#
#         # 엣지를 찾아냄
#         for edge in self.edges[node_type]:
#             if target_node == edge.get_target_node():
#                 self.edges[node_type] = self.edges[node_type](without this edge)
#                 return
#
#     3. get_edges():
#         edge_list = []
#         for node_type in edges.keys()
#             edge_list = edge_list + edges.edges[node_type]
#         return edge_list
#
# Graph 베이스 노드 클래스
class BaseNode:
    def __init__(self, node_type):
        self.edges = {}     # 엣지 해시 테이블
        self.node_type = node_type  # 노드 타입  -> 중요함. 이게 엣지를 담는 위치를 정해준다

    # Edge 추가 함수
    # node_type 필요 함. (protected)
    def _add_edge(self,  target_node, gen_time):
        node_type = target_node.node_type
        # 엣지를 담는 곳이 잘못 되었다면 False 를 반환
        # 상속받은 클래스에서 Edge 키를 정의 했기에 가능함
        if node_type not in self.edges:
            return False

        edge = Edge(target_node=target_node, gen_time=gen_time)            # 엣지 생성
        # 엣지가 존재하는 것만으로 판단하여 생성할 것인지 아닌지를 판단
        if edge not in self.edges[node_type]:
            self.edges[node_type].append(edge)                                 # 엣지 담기
            return True
        return False

    # Edge 제거 함수 (protected)
    def _remove_edge(self,  target_node):
        # 리스트 컴프리헨션으로 작성하여, 조금 더 빠른 반복문 실행으로 만들었음
        # 실상 성능의 차이는 좀 적긴하다.
        node_type = target_node.node_type
        # 엣지를 담은 장소가 잘못되어있다면 바로 턴
        if node_type not in self.edges:
            return False

        # 엣지 찾기
        for edge in self.edges[node_type]:
            if target_node == edge.get_target_node():
                self.edges[node_type].remove(edge)
                # self.edges[node_type] = [edge_2 for edge_2 in self.edges[node_type] if edge_2.get_target_node() == target_node]
                return True
        return False

    # 오버라이딩 용
    def get_id(self):
        pass

    def get_edges(self):
        edge_list = []
        for node_type in self.edges.keys():
            edge_list = edge_list + self.edges[node_type]
        return edge_list

    # # 이웃한 노드의 엣지 찾기
    # def __find_edge(self, target_node):
    #     node_type = target_node.node_type
    #     # 엣지를 담은 곳이 잘못되어있음.
    #     if node_type not in self.edges:
    #         return None
    #
    #     for edge in self.edges[node_type]:
    #         if target_node == edge.get_target_node():
    #             return edge
    #     return None
    #

    # 노드 삭제 시. edge까지 전부 삭제
    def __del__(self):
        self.edges.clear()

# class UserNode
#     1. initialize_variables(uid)
#         super().__init__()
#         uid = uid
#         edges["feed"] = []  # 노드 타입에 대한 엣지리스트를 정의
#
#     2. 아이디 얻기
#         # 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#         return uid
#
#     3. 엣지 추가 add_edge (내부 함수로 동작)
#         return self.__add_edge(target_node, gen_time)
#
#     4. 엣지 삭제 remove_edge (내부 함수로 동작)
#         return self.__remove_edge(target_node)

# 유저 노드
class UserNode(BaseNode):
    def __init__(self, uid):
        super().__init__("user")
        self.uid = uid
        self.edges["feed"] = [] # 엣지 리스트를 따로 생성한다. 중요하다

    # 노드의 일치성 판단. 이는 기록된 id를 가지고 판단
    def __eq__(self, other):
        return self.uid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 유저 아이디 얻기
    def get_id(self):
        return self.uid

    # 엣지 추가
    def add_edge(self, target_node, gen_time:datetime):
        # 이 작업이 True, False를 반환 하기에 이렇게 함.
        return self._add_edge(target_node, gen_time)

    # 엣지 삭제, 이 작업은 나의 엣지만 없애는 작업. 상대노드꺼는 그래프에서 작업
    def remove_edge(self, target_node):
        # 노드 타입이 Feed 일 때만 수행
        return self._remove_edge(target_node)

# class HashNode
#     1. initialize_variables(hid)
#         super().__init__()
#         hid = hid
#         edges["feed"] = []  #  노드 타입에 대한 엣지리스트를 정의
#
#     2. 아이디 얻기
#         # 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#         return hid
#
#     3. 엣지 추가 add_edge (내부 함수로 동작)
#         return self.__add_edge(target_node, gen_time)
#
#     4. 엣지 삭제 remove_edge (내부 함수로 동작)
#         return self.__remove_edge(target_node)

# 해시태그 노드
class HashNode(BaseNode):
    def __init__(self, hid):
        super().__init__("hashtag")
        self.hid = hid          # 해시태그 아이디, 문자열이 된다.
        self.edges["feed"] = []

        # 추가된 해시태그의 사용량 체크
        self.weight = 0         # Ranking에 사용되는 값인데 계산하는 함수가 따로 있음
        self.trend= {
            "now":0,            # 기준시간 ~ 1시간까지의 사용량 체크
            "prev":0            # 1시간 후 ~ 2시간 후 사용량 체크. 이전의 사용량 체크
        }

    # 노드 일치성 판단. 기록된 id를 통해 판단
    def __eq__(self, other):
        return self.hid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {}, {})'.format(self.get_id(), self.node_type, self.weight)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {}, {})'.format(self.get_id(), self.node_type, self.weight)

    # 아이디 반환 함수
    def get_id(self):
        return self.hid

    # Weight를 업 시킴
    # 글을 작성하는 시점 = Weight 중, now가 증가하는 시점
    # Feed를 수정하여, 새로운 해시태그가 생성될 때에도 이 함수가 적용
    def weight_up(self):
        self.trend["now"] += 1

    # Weight의 상태가 업데이트.
    # Weight는 recommend Manager에서 업데이트됨
    def weight_update(self, new_weight):
        self.weight = new_weight
        self.trend["prev"] = self.trend["now"]
        self.trend["now"] = 0

    # 엣지 추가
    def add_edge(self, target_node, gen_time:datetime):
        return self._add_edge(target_node, gen_time) # 엣지 추가

    # 엣지 삭제, 이 작업은 나의 엣지만 없애는 작업. 상대노드꺼는 그래프에서 작업
    def remove_edge(self, target_node):
        return self._remove_edge(target_node)

# class FeedNode
#     1. initialize_variables(fid)
#         super().__init__()
#         fid = fid
#         # 긴급 추가 (write_uid 정보를 feed 그래프 내에서 찾아오는 방법이 없어서 feed node 추가 시, 이것도 같이 들고옴.
#         write_uid = write_uid
#         edges["user"] = []  #  노드 타입에 대한 엣지리스트를 정의
#         edges["hashtag"] = []
#
#     2. 아이디 얻기
#         # 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#         return fid
#
#     3. 엣지 추가 add_edge (내부 함수로 동작)
#         return self.__add_edge(target_node, gen_time_str)
#
#     4. 엣지 삭제 remove_edge (내부 함수로 동작)
#         return self.__remove_edge(target_node)


# 피드 노드
class FeedNode(BaseNode):
    def __init__(self, fid, write_uid):
        super().__init__("feed") # 상속
        self.fid = fid          # Feed id
        self.write_uid = write_uid      # 작성한 User id
        self.edges["user"] = []
        self.edges["hashtag"] = []

    # 노드 일치 비교
    def __eq__(self, other):
        return self.fid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 노드 아이디 얻기
    def get_id(self):
        return self.fid

    # 엣지 추가
    def add_edge(self, target_node, gen_time:datetime):
        result = self._add_edge(target_node, gen_time)
        return result

    # 엣지 삭제
    def remove_edge(self, target_node):
        result = self._remove_edge(target_node)
        return result

# class FeedChaosGraph
#     1. initalize_variables
#
#     2. Call 함수 정의
#         all_node_feeds = self.num_feed_nodes + self.num_user_nodes + self.num_hash_nodes
#         pprint(f'{YELLOW}INFO{RESET}<-[    {all_node_feeds} NOVA Graph IN SEARCH ENGINE NOW READY')
#         pprint(f'           {self.num_feed_nodes} feed nodes,')
#         pprint(f'           {self.num_user_nodes} user nodes,')
#         pprint(f'           {self.num_hash_nodes} hash nodes,')
#
#     3. 노드 존재 여부 확인(node_id, tree)
#         return booltype if tree.get(id)
#
#     4. 엣지 찾기(source, target) (내부 함수)
#         edge_list = source.get_edges()
#         for edge in edge_list:
#             edge.target_node == target:
#                 return True
#         return False
#
#     5. add_edge(source, target, date) (내부 함수)
#         source.add_edge(target, date)
#         target.add_edge(source, date)
#
#     6. remove_edge(source, target) (내부 함수)
#         source.remove_edge(target)
#         target.remove_edge(source)
#
#     7. add_node(노드 타입, 노드 아이디, 트리)
#         if tree에 노드가 존재한다면:
#             이미 존재하는 노드 반환
#
#         아니면:
#         노드 생성
#         트리에 노드를 insert
#
#     8. remove_node(노드, 트리):
#        edge_list = 노드.get_edges()
#
#         for edge in edge_list:
#             opponent = edge.target_node()
#             self.__remove_edge(node, opponent)
#
#         node_type = node.node_type
#         node_id = node_id
#         del node
#
#         노드 숫자 줄이기
#         tree.remove(node_id)
#
#     9. connect_feed_with_hashs( 피드, 해시노드들, 생성 날짜)
#         모든 해시태그에 대해
#         엣지를 생성함
#
#     10. sync_feed_with_hashs (노드, 새로운 해시노드들):
#     해시노드 엣지 리스트를 들고옴 (옛날 해시 + 새로운 해시)
#
#         for edge in edge_list:
#             target_node = edge.target_node
#             if not target_node in new_hash_nodes:
#                 remove_edge(feed, target)
#
#     11. disconnect_feed_with_hash ( 피드, 해시노드 ):
#         __remove_edge(feed, hash)
#
#     12. connect_feed_with_user ( 피드, 유저노드):
#         엣지 생성
#
#     13. disconnect_feed_with_user(피드, 유저 노드):
#         엣지 삭제
#
#     14. feed_recommend_user(start_fid, max_user_find=10, max_feed_find=5):
#         1. 시작하는 노드를 찾아냄
#         2. 시작한 노드에서 뻗어나가는 엣지들을 찾아냄
#         3. 가장 최신의 엣지순서대로 정렬한 후, 상위 10개만 잡아냄
#         4. 그 엣지들을 잇는 User들에게 이어진 Feed 노드 엣지 집합 찾아냄
#         5. 그 Feed 엣지들도 다시 최신의 순서대로 정렬 후, 상위 5개 만 집어내서
#         5-1. 이 때, source노드에서 이어진 edge는 제외해야한다.
#         6. 결과 리스트에 담음. 이 때, fid만 담아내어, 나중에 언제든지 참조하기 편하게 한다.
#         return recommend_list
#
#     15. feed_recommend_hash(start_fid, max_hashtags=4, max_feed_find=10):
#         1. 시작노드 찾아냄
#         2. 시작노드에서 뻗어나간 해시태그 엣지들을 찾음
#         3. 기준은 해시태그에 연결되어 있는 Feed들이 많은 순으로 정렬해서 상위 4개 정도 뽑아 옴
#         4. 연결된 해시태그가 가장 최신으로 연결된 랜덤 Feed 10개 까지 뽑아온다.
#         똑같이, 자신에게 붙은 edge는 제외한다.
#         5. recommend_list에 담고, 반환
#         return recommend_list

# 피드-유저-해시태그 통합 그래프
class FeedChaosGraph:
    def __init__(self):
        self.num_feed_nodes = 0
        self.num_user_nodes = 0
        self.num_hash_nodes = 0

    def __call__(self):
        all_node_feeds = self.num_feed_nodes + self.num_user_nodes + self.num_hash_nodes
        pprint(f'{YELLOW}INFO{RESET}<-[    {all_node_feeds} NOVA Graph IN SEARCH ENGINE NOW READY')
        pprint(f'           {self.num_feed_nodes} feed nodes,')
        pprint(f'           {self.num_user_nodes} user nodes,')
        pprint(f'           {self.num_hash_nodes} hash nodes,')

    # 노드 존재 여부 확인
    # noinspection PyMethodMayBeStatic
    def __is_node_exist(self, node_id, tree) -> bool:
        if tree.get(node_id):
            return True
        return False

    # edge 찾기
    # noinspection PyMethodMayBeStatic
    def __find_edge(self, source_node, target_node):
        edge_list = source_node.get_edges()

        for edge in edge_list:
            if edge.get_target_node() == target_node:
                return True
        return False

    # 엣지 추가
    # noinspection PyMethodMayBeStatic
    def __add_edge(self, source_node, target_node, gen_time):
        source_node.add_edge(target_node, gen_time)
        target_node.add_edge(source_node, gen_time)

    # 엣지 삭제
    # noinspection PyMethodMayBeStatic
    def __remove_edge(self, source_node, target_node):
        source_node.remove_edge(target_node)
        target_node.remove_edge(source_node)

    # 노드 추가
    def add_node(self, node_type, node_id, tree:AVLTree, write_uid:str=""):
        node = None

        # 만약 노드가 이미 트리에 있다면, 이미 만들어진 노드를 반환
        if self.__is_node_exist(node_id=node_id, tree=tree):
            return tree.get(node_id)

        # 노드 생성
        if node_type == "user":
            node = UserNode(node_id)
            self.num_user_nodes += 1
        elif node_type == "hashtag":
            node = HashNode(node_id)
            self.num_hash_nodes += 1
        elif node_type == "feed":
            # feed 노드만의 특징, 작성한 유저의 아이디를 또하나의 값으로 가진다, 기본값은 ""로 한다.
            node = FeedNode(node_id, write_uid)
            self.num_feed_nodes += 1

        # 노드 추가
        tree.insert(key=node_id, value=node)
        return node

    # 노드 삭제
    def remove_node(self, node, tree:AVLTree):
        edge_list = node.get_edges()

        for edge in edge_list:
            opponent_node = edge.get_target_node()
            self.__remove_edge(node, opponent_node)

        # 자신이 제거되면서 자신에게서 출발하는 모든 엣지가 가비지 컬렉팅으로 사라짐
        node_type = node.node_type
        node_id = node.get_id()
        del node

        if node_type == "user":
            self.num_user_nodes -= 1
        if node_type == "hashtag":
            self.num_hash_nodes -= 1
        if node_type == "feed":
            self.num_feed_nodes -= 1

        tree.remove(key=node_id)
        return True

    # Feed-Hash 간 엣지 연결 함수 # 수정 필요. 이미 엣지가 연결되어 있는지 확인이 필요함
    def connect_feed_with_hashs(self, feed_node, hash_nodes, date):
        for hash_node in hash_nodes:
            if not self.__find_edge(feed_node, hash_node):
                self.__add_edge(feed_node, hash_node, date)

        return

    # Feed-new hashtags 엣지 수정, 기존의 엣지 중, 없어진 해시태그는 삭제된다.
    def sync_feed_with_hashs(self, feed_node, new_hash_nodes):
        edge_list = feed_node.edges["hashtag"]

        # 이 때, 기존의 해시태그와 새로운 해시태그 모두 연결되어 있음
        for edge in edge_list:
            # 리스트 안에 있는 에지들을 모두 비교
            target_node = edge.get_target_node()
            # 연결된 노드가 새로운 해시 조합에 해당되지 않는다면 엣지 삭제
            if not target_node in new_hash_nodes:
                self.__remove_edge(feed_node, target_node)

        return

    # Feed-Hash 간의 연결을 끊음
    def disconnect_feed_with_hash(self, feed_node, hash_node):
        if self.__find_edge(feed_node, hash_node):
            self.__remove_edge(feed_node, hash_node)
            return True
        return False

    # 유저 노드와 Feed 노드의 연결
    def connect_feed_with_user(self, feed_node, user_node, date):
        if not self.__find_edge(feed_node, user_node):
            self.__add_edge(feed_node, user_node, date)
        return

    # 유저 노드와 Feed 노드 간 연결을 끊음
    def disconnect_feed_with_user(self, feed_node, user_node):
        if self.__find_edge(feed_node, user_node):
            self.__remove_edge(feed_node, user_node)
            return True
        return False

    # 피드-유저 사이에서 찾아내는 유사한 피드

    # 1단계 : 유저 상위 10명 집계
    # 2단계 : 유저 담기. 방문한 Feed_id 집계 : list()
    #	가장 중요한 건, 글쓴이에 대해서는 집계하지 않는다.
    #
    # 3단계 : 첫번째 줄에서 유저에 대한 feed 집계. 중복을 고려해 10개로 늘리고.
    # 	set()을 최대한 활용해 중복을 지워나가는 방향으로 잡는다
    #	방문했던 feed임이 확인되면, 가차없이 지워야함. 왜냐하면 똑같은 노드가 발생할 수 있기 때문.
    #	따라서, Set()을 사용한다.
    #
    # for user_node in user_queue:
    #	sorted_edges = sorted(user_node.edges["feed"])[:max_feed]
    #	for edge in sorted_edges:
    #		# 어짜피 set()을 사용하기 때문에, 중복은 알아서 없어짐
    #		related_fid = edge.target.id()
    #		if not in visited_feed:
    #			recommend_list.append(related_fid)
    #
    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_like_user(self, start_node:FeedNode, max_user_find=10, max_feed_find=8):
        # 가장 먼저, Feed를 확인
        recommend_list = set()
        user_queue = []


        # 각 연결된 유저 edge를 찾음
        sorted_edges_latest_related = sorted(start_node.edges["user"])[:max_user_find]
        # 그 중, 가장 최근에 Feed에 관심을 가진(좋아요를 누른) 유저들 10명을 추려냄
        for edge in sorted_edges_latest_related:
            # 진짜 만약에 연결된 edge중에서 작성자와 연결된 edge들이 있을 경우, 그 노드만을 제외하고 추가한다.
            # 즉, 하나의 유저만 걸러지는 방법.
            if edge.target_node.get_id() != start_node.write_uid:
                user_queue.append(edge.target_node)

        # 이제, 그 유저들과 연결된 Feed를 담아내는 과정
        for user_node in user_queue:
            # 최신 순으로 정렬된 엣지 중에서, 최대 5개의 feed들을 가져올 것
            sorted_edges_latest_relate_feed = sorted(user_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edges_latest_relate_feed:
                # 가져온 Edge에서 Feed id를 추출하여 recommend_list에 담음
                related_feed_id = edge.get_target_node().get_id()
                recommend_list.add(related_feed_id)


        # 시작Feed가 다시 추천리스트에 들어가는 것을 방지하기 위해 recommend_list에서 삭제 진행
        recommend_list.discard(start_node.fid)   # discard 쓰는 이유 (set()에 있을수도 있고, 없을 수도 있음. GPT 피셜임)

        return list(recommend_list)

    # 피드-해시태그 사이에서 찾아내는 유사한 피드

    # 1단계 : 시작한 Feed에 대한 해시태그 최대 4개에 대해 Edge 수집
    # 2단계 : Hash태그 담기. 방문한 Feed는 집계해야됨.
    # 3단계 : 해시태그에 대해 Feed를 집계함. 가장 최신의 글을 먼저 집계한다.
    #	여기서도 방문했던 Feed는 가차없이 지워야한다. (물론 이는 History에서 관리된다.)
    #	set()을 이용해 중복된 Feed는 지워내면서 추가하면 된다.
    #
    # for hash_node in hash_queue:
    #	sorted_edges = sorted(hash_node.edges["feed"])[:max_feed]
    #	for edge in sorted_edges:
    #		related_fid = edge.target.id()
    #		recommend_list.add(related_fid)
    #
    # 4단계 : 내가 본 Feed는 전부 쳐내야함.

    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_hashtag(self, start_node:FeedNode, max_hash=4, max_feed_find=5):
        recommend_list = set()
        hash_queue = []

        # 각 연결된 hash노드 엣지를 찾아냄
        sorted_edges_latest_related_hash = sorted(start_node.edges["hashtag"])[:max_hash]

        # 여기서 이제 해시태그 노드들을 얻어냄
        for edge in sorted_edges_latest_related_hash:
            hash_queue.append(edge.target_node)

        # 다시, 해시노드와 연관된 Feed와 연결된 엣지를 찾아냄
        for hash_node in hash_queue:
            # 최신 순으로 정렬된 edge들을 가져옴
            sorted_edges_latest_related_feed = sorted(hash_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edges_latest_related_feed:
                # 가져온 Feed Edge에서 feed id를 추출해 recommend_list를 다음
                related_feed_id = edge.get_target_node().get_id()
                recommend_list.add(related_feed_id)

        # 시작Feed가 다시 추천리스트에 들어가는 것을 방지하기 위해 recommend_list에서 삭제 진행
        recommend_list.discard(start_node.fid)   # discard 쓰는 이유 (set()에 있을수도 있고, 없을 수도 있음. GPT 피셜임)

        return list(recommend_list)

    # User의 좋아요에 따라 Feed를 추천하는 시스템

    # 1단계: 로그인한 유저에게로부터 좋아요로 태깅된 Edge들을 통해 좋아요를 누른 Feed들을 모음
    # 2단계: 그렇게 모은 Feed들은 이미 본 Feed들이기 때문에 추천 feed에는 집계하지 않지만, 이 Feed들에 좋아요를 남긴 유저들을 찾는데 쓰임
    #   따라서, Feed에 좋아요를 남긴 유저들을 모음.
    # 3단계 : 이렇게 해서 모인 유저들에 따라, 좋아요한 Feed를 담음. 이 때, 내가 좋아요를 남겨서 찾아온 Feed에 대해서는 담지않음

    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_me(self, watch_me:UserNode, max_like=10, max_related_user=4, max_feed_find=5):
        # 비로그인 유저는 빈 리스트를 반환
        if watch_me.get_id() == "":
            return []


        # 중복된 Feed를 방지하기 위해서
        recommend_list = set()
        visited_like_feeds = []
        # 내가 좋아한 Feed들에 대해 같은 유저가 다른 2개의 Feed들도 동시에 좋아할 수 있음
        # visited like_user_queue는 user가 변할수 있는 노드이기 떄문에 set() 사용x
        # 오류가 발생한 부분, unhashable Error
        # 잘못된 Set()의 사용이 불러온 오류임.
        like_user_queue = [watch_me]

        # 최대 10개 의 좋아요한 Feed나, 작성한 feed에 대한 리스트를 불러옴
        sorted_edges_latest_like_feed = sorted(watch_me.edges["feed"])[:max_like]

        # visited_like_feed를 분리해놓는 이유
        # 구분하기 편하라고요
        for edge in sorted_edges_latest_like_feed:
            visited_like_feeds.append(edge.target_node)

        # 유저들을 골라내는 과정
        for visited_feed in visited_like_feeds:
            sorted_edge_feed_like_user = sorted(visited_feed.edges["user"])[:max_related_user]
            for edge in sorted_edge_feed_like_user:
                # 시작된 본인만 아니라면 모두 OK
                # 리스트에 이미 UserNode가 담겨있는 상태라면, 담지 않아도 된다.
                if edge.target_node.get_id() != watch_me.get_id() and edge.target_node not in like_user_queue:
                    like_user_queue.append(edge.target_node)


        # 골라낸 유저 중
        for like_user_node in like_user_queue:
            sorted_edge_like_feed = sorted(like_user_node.edges["feed"])[:max_feed_find]

            for edge in sorted_edge_like_feed:
                if edge.target_node not in visited_like_feeds:
                    related_fid = edge.target_node.get_id()
                    recommend_list.add(related_fid)

        return list(recommend_list)

    # HashTag 랭킹에 관해 Feed를 추출하는 시스템
    # Feed 해시태그 랭킹에 집계된 Hash태그들과 연결된 Feed들을 무작위로 추첨
    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_ranking(self, hash_tree:AVLTree, hashtag_rank:list, top_n_hashtags=5, max_feed_find=6):
        hashtag_top_n = hashtag_rank[:top_n_hashtags]
        recommend_list = set()

        for hashtag in hashtag_top_n:
            hash_node = hash_tree.get(key=hashtag)
            sorted_edge = sorted(hash_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edge:
                recommend_list.add(edge.target_node.get_id())

        return list(recommend_list)

#
# class FeedAlgorithm:
#     Feed 추천을 위해 만들어진 알고리즘을 담는 곳
#     여기서는 그래프와 데이터들을 담고 있음
#     __init__(database):
#           feed_chaos_graph = FeedChaosGraph()
#           feed_avltree = AVLTree()
#           user_avltree = AVLTree()
#           hash_avltree = AVLTree()
#           __initialize_graph()
#
#     __str__():
#         출력 포맷 설정
#
#     get_nodes_list():
#         노드에 대한 정보 공개
#
#     1. initialize_all_feeds(database):
#         1) 데이터들을 모두 객체화함
#         2) 데이터들을 모두 테이블에 담는다.
#         3) 데이터에 담긴 해시들을 꺼내서 set()에 담는다.
#
#     2. initialize_user_table(database):
#         1) 유저 데이터들을 모두 불러와서 객체화
#         2) 유저 테이블에 담는다.
#
#     3. initialize_graph(self):
#         graph_initialize화를 함.
#
#     4. graph_nodes_print():
#         print(self.__feed_chaos_graph.nodes)
#
#     5. graph_add_feed_node(feed):
#         1) 피드테이블에 새롭게 생긴 피드를 추가
#         2) 피드 노드를 생성하고, 그래프에 추가한다.
#         3) 피드에 저장된 해시태그마다 테이블에 담고, 해시태그 노드를 만들어낸다.
#         4) 글을 작성한 유저 노드를 찾아서 엣지를 연결한다. (이 때, 유저 노드가 없으면 실패)
#
#     6. graph_add_user_node(user):
#         1) 유저테이블에 있는지 확인
#         2) 없으면 노드를 만들어 붙임
#
#
#     7. Graph_remove_node(node_id):
#         1) 먼저 id를 통해 일치하는 노드들을 찾는다.
#         2) 노드를 삭제한다.
#         3) 노드타입에 따라 테이블도 삭제
#
#     8. Graph_remove_edge(source_id, target_id):
#         1) 노드 찾기 (소스노드, 타겟노드)
#         2) 엣지 삭제
#
#     9. find_recommend_feed(start_fid):
#         1) 유저-feed 관계를 바탕으로 한 리스트 추출
#         2) 해시태그-feed 관계를 바탕으로 한 리스트 추출
class FeedAlgorithm:
    def __init__(self, database):
        self.__feed_chaos_graph = FeedChaosGraph()
        self.__feed_node_avltree = AVLTree()
        self.__user_node_avltree = AVLTree()
        self.__hash_node_avltree = AVLTree()
        self.__initialize_graph(database=database)

    def __str__(self):
        all_node_feeds = len(self.__feed_node_avltree) + len(self.__user_node_avltree) + len(self.__hash_node_avltree)
        return (f"{YELLOW}INFO{RESET}<-[    {all_node_feeds} nodes in NOVA Graph IN SEARCH ENGINE NOW READY\n")
        #f"             {list(self.__feed_node_avltree.values())} feed node in Graph.\n" +
        #f"             {list(self.__user_node_avltree.values())} user node in Graph.\n" +
        #f"             {list(self.__hash_node_avltree.values())} hash node in Graph.\n" )

    # uid로 유저 노드 찾기
    def get_user_node_with_uid(self, uid:str):
        return self.__user_node_avltree.get(key=uid)

    def get_user_nodes(self):
        return list(self.__user_node_avltree.values())

    def get_feed_nodes(self):
        return list(self.__feed_node_avltree.values())

    def get_hash_nodes(self):
        return list(self.__hash_node_avltree.values())

    def __initialize_graph(self, database):
        user_datas = database.get_all_data(target="uid")
        feed_datas = database.get_all_data(target="fid")
        user_list = []
        feed_list = []

        # 빈 유저를 생성 후, 추가하는 과정
        null_user = User()
        self.add_user_node(null_user)

        # 유저 데이터 문자열 딕셔너리 -> User() 변환
        for user_data in user_datas:
            single_user = User()
            single_user.make_with_dict(dict_data=user_data)
            user_list.append(single_user)

        # 유저 데이터를 먼저 Graph와 트리에 추가
        for user in user_list:
            self.add_user_node(user)

        # 피드 데이터를 객체화
        for feed_data in feed_datas:
            single_feed = Feed()
            single_feed.make_with_dict(dict_data=feed_data)
            feed_list.append(single_feed)

        # Feed 데이터 노드를 추가
        for feed in feed_list:
            self.add_feed_node(feed)

        all_node_feeds = len(self.__feed_node_avltree) + len(self.__user_node_avltree) + len(self.__hash_node_avltree)
        print(f'{YELLOW}INFO{RESET}<-[      {all_node_feeds} nodes in NOVA Graph IN SEARCH ENGINE NOW READY')

        #$print(f"             {list(self.__feed_node_avltree.values())} feed node in Graph.")
        #$print(f"             {list(self.__user_node_avltree.values())} user node in Graph.")
        #$print(f"             {list(self.__hash_node_avltree.values())} hash node in Graph.")

        return

    # 해시 노드들 추가 # 트리 안에 있는 해시태그를 발견하면 기존의 노드를 반환하도록 한다. 수정필요
    def __add_hash_nodes(self, hashtags:list):
        hash_nodes = []
        for hashtag in hashtags:
            # 해시 태그 마다 노드를 생성
            # 중요한 점 : 노드가 이미 생성되어있으면, 기존의 노드를 반환 받음
            hash_node = self.__feed_chaos_graph.add_node(node_type="hashtag", node_id=hashtag, tree=self.__hash_node_avltree)

            # hashtag의 사용량을 갱신
            hash_node.weight_up()

            # 반환할 노드
            hash_nodes.append(hash_node)

        return hash_nodes

    # Feed 중 랜덤하게 샘플을 골라서
    def __random_feed_sample(self, samples_feed_n=15):
        feeds_value = list(self.__feed_node_avltree.values())
        if len(feeds_value) <= samples_feed_n:
            return feeds_value
        return random.sample(feeds_value, samples_feed_n)

    # 유저 노드 추가 (테스트 O)
    def add_user_node(self, user:User):
        if self.__user_node_avltree.get(key=user.uid):
            return False

        # 이미 노드가 트리에 존재 함 -> 노드 객체가 전부 포인터로 이루어져 있어서 트리, 그래프 모두 있음
        user_node = self.__feed_chaos_graph.add_node(node_type="user", node_id=user.uid, tree=self.__user_node_avltree)
        return user_node

    # Feed 노드 추가
    def add_feed_node(self, feed:Feed):
        if self.__feed_node_avltree.get(key=feed.fid):
            return "case1"


        write_uid = feed.uid
        hashtags = feed.hashtag     # feed에 담긴 해시태그
        gen_time = datetime.strptime(feed.date, '%Y/%m/%d-%H:%M:%S')

        # 피드 노드 생성
        # FeedNode는 다른 노드들과 달리 특수한 id값인 작성자id를 가지게 된다.

        feed_node = self.__feed_chaos_graph.add_node(node_type="feed", node_id=feed.fid, write_uid=write_uid, tree=self.__feed_node_avltree)
        # 해시 노드 생성 (해시 노드들은 생성이 될 때, 이미 존재하는 노드들이라면 그 노드를 반환함
        hash_nodes = self.__add_hash_nodes(hashtags=hashtags)

        # Feed - 해시노드 간 edge 생성
        self.__feed_chaos_graph.connect_feed_with_hashs(feed_node=feed_node, hash_nodes=hash_nodes, date=gen_time)

        # 글을 쓸 때, 작성자가 트리안에 있어야만 가능.
        if feed.uid not in self.__user_node_avltree:
            return "case2"
        user_node = self.__user_node_avltree.get(feed.uid)

        # 작성한 글쓴이와 Feed 연결
        self.__feed_chaos_graph.connect_feed_with_user(feed_node=feed_node, user_node=user_node, date=gen_time)

        return "case success"

    # Feed 노드 삭제
    def remove_feed_node(self, fid):
        # 해당하는 Feed가 존재히지 않는 경우, False를 반환
        feed_node = self.__feed_node_avltree.get(key=fid)
        if not feed_node:
            return False
        return self.__feed_chaos_graph.remove_node(node=feed_node, tree=self.__feed_node_avltree)

    # 유저 노드 삭제
    def remove_user_node(self, uid):
        # 만약 uid에 해당하는 노드가 존재하지 않는다면 삭제할 수 없으니 False를 반한
        user_node = self.__user_node_avltree.get(key=uid)
        if not user_node:
            return False
        return self.__feed_chaos_graph.remove_node(node=user_node, tree=self.__user_node_avltree)

    # feed_node 해시 태그 수정
    def modify_feed_node(self, feed:Feed):
        if feed.fid not in self.__feed_node_avltree:
            return False

        # 이미 수정된 Feed를 가지고 진행, 즉, Feed 수정 버튼을 누른 직후에 일어나는 일
        feed_node = self.__feed_node_avltree.get(key=feed.fid)

        # 새롭게 작성된 해시태그들
        new_hashtags = feed.hashtag
        feed_date = datetime.strptime(feed.date, '%Y/%m/%d-%H:%M:%S')

        # 새로운 해시태그들에 대한 노드들과 edge가 생성
        new_hash_nodes = self.__add_hash_nodes(hashtags=new_hashtags)
        self.__feed_chaos_graph.connect_feed_with_hashs(feed_node=feed_node, hash_nodes=new_hash_nodes, date=feed_date)

        # 새롭게 연결된 새로운 해시노드들과 비교하여 옛날의 해시태그의 엣지들을 끊어내는 작업
        self.__feed_chaos_graph.sync_feed_with_hashs(feed_node=feed_node, new_hash_nodes=new_hash_nodes)

        return True

    # 좋아요를 누른 게시글과 유저 잇기
    def connect_feed_like_user(self, uid, fid, like_time):
        if uid not in self.__user_node_avltree or fid not in self.__feed_node_avltree:
            return False
        user_node = self.__user_node_avltree.get(key=uid)
        feed_node = self.__feed_node_avltree.get(key=fid)

        self.__feed_chaos_graph.connect_feed_with_user(feed_node=feed_node, user_node=user_node, date=like_time)
        return True

    # 좋아요를 해제한 게시글과 유저 엣지 제거
    def disconnect_feed_like_user(self, uid, fid):
        user_node = self.__user_node_avltree.get(key=uid)
        feed_node = self.__feed_node_avltree.get(key=fid)
        return self.__feed_chaos_graph.disconnect_feed_with_user(feed_node=feed_node, user_node=user_node)

    # 추천 feed를 찾아줌
    def recommend_next_feed(self, start_fid:str, mine_uid:str, hashtag_ranking:list, history:list):

        # 추천 Feed를 찾을 때, 다음의 경우를 고려했어야 했음.
        # 문제점 : 노드에 연결된 엣지가 부득이하게 하나만 존재하는 경우

        # 1. Feed에 좋아요가 있고, 해시태그들이 다양함.
        # 2. Feed에 좋아요가 없지만, 해시태그들이 다양함.
        # 3. Feed에 좋아요는 있지만, 해시태그가 하나만 붙음. (타고온 노드만)
        # 4. Feed에 좋아요도 없고, 해시태그도 진짜 희귀한 경우 (진짜 알고리즘을 타고와서 겨우발견할 법한 글)

        # 1의 경우. 이미 다양한 경우에 대해, Feed를 추천 받고 있음.
        # 2의 경우, 해시태그들의 경우에서 Feed를 받을 수 있음.
        # 3의 경우, 좋아요에 관해서 Feed 추천을 받을 수 있음.
        # 4의 경우, DB안에 있는 무작위의 Feed를 골라내야함

        # 만약에 두 상황에서 모두 뽑지 않았다. 이제 유저 본인에 대한 좋아요를 눌렀던 Feed내에서 찾기 시작해야함.


        # 그래야 더 다양한 주제에 대한 Feed를 추천 받을 수 있다.
        # 즉, Feed->User가 아닌 User->Feed 시스템이라는 점

        # 5. 로그인된 유저 본인에게 좋아요를 누른 Feed들을 기점으로 움직이는 Feed 추천
        #  이 때, 본인에게서 시작되는 것은 자신이 작성한 글또한 모두 포함시켜서 Search를 하는데 그 대신, 최종 추천 Feed에는 추가되지 않도록 헤야함.

        # 6. HashTag 랭킹에 의해 집계되어 추천되는 Feed
        #   진짜 초기에 가입되서 아무것도 없는 경우, 혹은 저 위에서 HashTag 주제 전환을 위해서 Rank에 집계된 HashTag를 이용해 feed를 추천해준다.

        # 7. 무작위의 feed를 추천. 이는 랜덤한 feed 중 20개를 추첨해 리스트에 담는다.
        # 진짜 무작위로 뽑아야됨.

        # Start 노드에 대한 Feed를 찾아냄.
        start_feed_node = self.__feed_node_avltree.get(key=start_fid)

        # 1, 2, 3, 4에 대한 경우
        # 매개의 중심은 내가 보고있는 Feed라는 점

        # User-Feed 간의 관계를 이용해 찾음
        # Hash-Feed 간의 관계를 이용해 찾음
        user_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_like_user(start_node=start_feed_node)
        hash_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_hashtag(start_node=start_feed_node)

        # 5에 대한 경우.
        # User가 Like했던 Feed들을 중심으로 찾음
        # 매가의 중심은 현재 Feed를 보고 있는 "나"라는 점.

        my_user_node = self.__user_node_avltree.get(mine_uid)
        me_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_me(watch_me=my_user_node)

        # 6. 해시태그 랭킹에 대한 추천
        ranking_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_ranking(
            hash_tree=self.__hash_node_avltree,
            hashtag_rank=hashtag_ranking
        )


        # 7. 완전 무작위 Feed List 추출.
        # 15개 정도의 무작위 Feed를 추출해내서 추천 Feed 리스트에 담음
        # AVLTree에서 뽑아서 씀

        random_feed_samples = self.__random_feed_sample()

        # Feed를 찾은 리스트들을 모두 합함.
        result_fid_list = user_feed_recommend_list + hash_feed_recommend_list + me_feed_recommend_list + ranking_feed_recommend_list + random_feed_samples

        # 히스토리에 존재하는 피드, 즉, 이전, 현재까지 본 모든 Feed들을 제외해야함
        for fid in result_fid_list:
            if fid not in history:
                return fid

        return None
