from datetime import datetime, timedelta

#def calculate_timeblocks_with_update(start_date, start_time, end_date, end_time):
    ## 시작 및 종료 시간 합치기
    #start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y/%m/%d %H:%M")
    #end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y/%m/%d %H:%M")

    ## 시간 구간 정보 (0-6, 6-12, 12-18, 18-24)
    #time_ranges = [(0, 6), (6, 12), (12, 18), (18, 24)]
    #timeblocks = []

    #current_datetime = start_datetime
    #first_block = True  # 첫 번째 블록인지 확인하는 플래그
    #end_flag = False

    #while current_datetime < end_datetime:
        ## 현재 시간의 구간 판별
        #hour = current_datetime.hour
        
        #if end_flag:
            #break
        
        #for i, (start_hour, end_hour) in enumerate(time_ranges):
            
            #if start_hour <= hour < end_hour:
                
                ## 첫 번째 구간이 아닌 경우 제외
                #if (not first_block and i == 0):
                    #end_flag = True
                    #break
                
                #current_range_start = current_datetime.replace(hour=start_hour, minute=0, second=0, microsecond=0)
                
                ## 구간 끝나는 시간이 24이면 다음 날 00:00으로 설정
                #if end_hour == 24:
                    #current_range_end = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                #else:
                    #current_range_end = current_datetime.replace(hour=end_hour, minute=0, second=0, microsecond=0)

                ## 구간 종료 시간이 종료 시간보다 크면 종료 시간으로 제한
                #actual_end = min(end_datetime, current_range_end)

                ## 앞 부분 패딩 및 총 길이 계산
                #if current_datetime == current_range_start:
                    #padding_minutes = 0
                #else:
                    #padding_minutes = int((current_datetime - current_range_start).total_seconds() / 60)

                #total_minutes = int((actual_end - current_datetime).total_seconds() / 60)
                
                #timeblocks.append({
                    #"구간 번호": i,
                    #"앞 부분 패딩": padding_minutes,
                    #"총 길이": total_minutes
                #})

                ## 현재 시간을 다음 구간 시작으로 이동
                #current_datetime = actual_end
                #first_block = False# 첫 번째 구간이 끝났으므로 플래그 변경
                #break

    ## 하루를 넘어가면 start_date와 start_time을 업데이트
    #if start_datetime.day != end_datetime.day:
        #new_start_date = end_datetime.strftime("%Y/%m/%d")
        #new_start_time = "00:00"
        #updated_end_date = end_datetime.strftime("%Y/%m/%d")
        #updated_end_time = end_datetime.strftime("%H:%M")
    #else:
        #new_start_date = start_date
        #new_start_time = start_time
        #updated_end_date = end_date
        #updated_end_time = end_time

    #return timeblocks, (new_start_date, new_start_time, updated_end_date, updated_end_time)


## 예제 데이터
#start_date = "2025/03/04"
#start_time = "19:30"
#end_date = "2025/03/05"
#end_time = "04:00"

## 결과 계산
#timeblocks, updated_time_info = calculate_timeblocks_with_update(start_date, start_time, end_date, end_time)

## 결과 출력
#print("Timeblocks:")
#for block in timeblocks:
    #print(block)

#print("\nUpdated Time Information:")
#print(updated_time_info)


today = datetime.today()

print(today.weekday())
