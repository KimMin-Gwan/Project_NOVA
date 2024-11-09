# from datetime import datetime

# # 저장된 과거 날짜
# past_date_str = "2024/06/02-21:08:30"

# # 문자열을 datetime 객체로 변환
# past_date = datetime.strptime(past_date_str, "%Y/%m/%d-%H:%M:%S")

# # 오늘 날짜 가져오기
# current_date = datetime.now()

# # 날짜 차이 계산
# date_difference = current_date - past_date

# # 차이 출력
# print(f"두 날짜 간의 차이는 {date_difference.days}일 {date_difference.seconds // 3600}시간 {(date_difference.seconds % 3600) // 60}분입니다.")





# import heapq

# # 우선순위 큐 초기화
# priority_queue = []

# # 데이터 샘플: 딕셔너리 리스트
# data = [
#     {"id": 1, "likes": 50, "name": "item1"},
#     {"id": 2, "likes": 30, "name": "item2"},
#     {"id": 3, "likes": 40, "name": "item3"},
# ]

# # 딕셔너리를 우선순위 큐에 추가 (likes 값을 기준으로 정렬)
# for item in data:
#     heapq.heappush(priority_queue, (item['likes'], item))

# # 우선순위 큐에서 데이터 출력
# while priority_queue:
#     _, item = heapq.heappop(priority_queue)
#     print(item)

def test():
    list_a=[1,2,3,4]
    return list_a[3:0:-1]

print(test() )