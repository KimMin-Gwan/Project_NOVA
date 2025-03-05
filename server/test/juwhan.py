from datetime import datetime


today = datetime.today()
shorted_year = today.year % 100
        
first_day_of_month = datetime(today.year, today.month, 1)

# 해당 날짜와 첫 번째 날의 주 번호 계산
start_week = first_day_of_month.isocalendar()[1]  # 해당 달 첫 날의 주 번호
current_week = today.isocalendar()[1]             # 해당 날짜의 주 번호

# 현재 주가 3월 내의 몇 번째 주인지 계산
week_in_month = current_week - start_week + 1
        
# 만약 미래에 있는 사람이 2100에 산다면 이 곳의 코드를 고치면 됩니다
print(f'{shorted_year}년 {today.month}월 {week_in_month}주차')