from datetime import datetime, timedelta

def set_target_date():
    today = datetime.today()
    first_day_of_month = datetime(today.year, today.month, 1)

    # 월요일이 가장 빠른 날을 찾기 위해 이번 달 첫째 날부터 시작해서 월요일을 찾습니다.
    current_date = first_day_of_month
    while current_date.weekday() != 0:  # 0은 월요일을 나타냅니다.
        current_date += timedelta(days=1)

    # 해당 주가 1주차인지 계산합니다.
    start_week = current_date.isocalendar()[1]  # 해당 달 첫 번째 월요일이 속한 주 번호
    current_week = today.isocalendar()[1]       # 오늘 날짜의 주 번호

    # 현재 주가 이번 달 내 몇 번째 주인지 계산합니다.
    week_in_month = current_week - start_week + 1

    shorted_year = today.year % 100
    target_month = f'{shorted_year}년 {today.month}월'
    target_week = f'{week_in_month}주차'
    print(target_month)
    print(target_week)
    return

#set_target_date()


def get_monday_date(target_date: str) -> datetime:
    # 입력 날짜를 datetime 객체로 변환
    target_date = datetime.strptime(target_date, "%Y/%m/%d")
    
    # 오늘의 요일 계산 (0: 월요일, 6: 일요일)
    day_of_week = target_date.weekday()
    
    # 오늘 날짜에서 요일 값을 빼서 이번 주 월요일 계산
    monday_date = target_date - timedelta(days=day_of_week)
    
    # 월요일 날짜를 datetime 객체로 반환
    return monday_date

target_date = "2025/03/23"
monday = get_monday_date(target_date)
print("이번 주 월요일:", monday)