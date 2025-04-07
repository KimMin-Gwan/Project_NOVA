from datetime import datetime, timedelta
    
    
def calc_date(today:datetime):
        first_day_of_month = datetime(today.year, today.month, 1)
        #print(first_day_of_month)

        # 월요일이 가장 빠른 날을 찾기 위해 이번 달 첫째 날부터 시작해서 월요일을 찾습니다.
        current_date = first_day_of_month
        while current_date.weekday() != 0:  # 0은 월요일을 나타냅니다.
            current_date += timedelta(days=1)

        # 해당 주가 1주차인지 계산합니다.
        print(current_date)
        start_week = current_date.isocalendar()[1]  # 해당 달 첫 번째 월요일이 속한 주 번호
        current_week = today.isocalendar()[1]       # 오늘 날짜의 주 번호
        
        return start_week, current_week
        
        
def set_target_date(date=datetime.today().strftime("%Y-%m-%d")):
    
    today = datetime.strptime(date, "%Y-%m-%d")
    
    start_week, current_week = calc_date(today)
    
    if start_week > current_week:
        # 이번 주의 월요일이 today임
        today = today = today - timedelta(days=today.weekday())
        start_week, current_week = calc_date(today)
        
    print(start_week, current_week)


    # 현재 주가 이번 달 내 몇 번째 주인지 계산합니다.
    week_in_month = current_week - start_week + 1
        
    shorted_year = today.year % 100
        
    # 만약 미래에 있는 사람이 2100에 산다면 이 곳의 코드를 고치면 됩니다
    print(f'{shorted_year}년 {today.month}월')
    print(f'{week_in_month}주차')
    
    return

set_target_date("2025-03-03")