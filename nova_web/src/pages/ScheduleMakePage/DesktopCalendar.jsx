import { useEffect, useState } from "react";
import style from "./ScheduleMakePage.module.css";

const DesktopCalender = ({
  selectedBias, selectedDate, handleSelectDate, scheduleList
}) => {
  const weekDays = ["일", "월", "화", "수", "목", "금", "토"];

  // 현재 년/월 상태
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1); // JS는 0부터 시작 → +1
  const [weeks, setWeeks] = useState([]);
  const [day, setDay] = useState("");

  const [todayEffect, setTodayEffect] = useState({
    month : true,
    day : today.getDate()
  })

  // 달력 생성
  useEffect(() => {
    generateCalendar(year, month);
  }, [year, month, scheduleList]);

  const generateCalendar = (y, m) => {
    const firstDay = new Date(y, m - 1, 1).getDay(); // 시작 요일
    const lastDate = new Date(y, m, 0).getDate(); // 마지막 날짜

    const days = [];
    // 앞쪽 빈칸
    for (let i = 0; i < firstDay; i++) {
      days.push({ day: null });
    }
    // 날짜 채우기
    for (let d = 1; d <= lastDate; d++) {
      days.push({ day: d, body: scheduleList[d] ? scheduleList[d].title : ""});
    }
    // 뒤쪽 빈칸
    while (days.length % 7 !== 0) {
      days.push({ day: null });
    }

    // 7일 단위로 끊기
    const weekChunks = [];
    for (let i = 0; i < days.length; i += 7) {
      weekChunks.push(days.slice(i, i + 7));
    }

    setWeeks(weekChunks);
  };

  // 이전달 이동
  const handlePrevMonth = () => {
    if (month === 1) {
      setYear((prev) => prev - 1);
      setMonth(12);
    } else {
      setMonth((prev) => prev - 1);
    }

    if(month == (today.getMonth()+1)){
      setTodayEffect(
        {
          month: true,
          day : today.getDay()
        }
      )
    }else{
      setTodayEffect(
        {
          month: false,
          day : today.getDay()
        }
      )
    }
  };

  // 다음달 이동
  const handleNextMonth = () => {
    if (month === 12) {
      setYear((prev) => prev + 1);
      setMonth(1);
    } else {
      setMonth((prev) => prev + 1);
    }

    if(month == (today.getMonth()+1)){
      setTodayEffect(
        {
          month: true,
          day : today.getDay()
        }
      )
    }else{
      setTodayEffect(
        {
          month: false,
          day : today.getDay()
        }
      )
    }
  };

  const trySelectDay = (day) =>{
    setDay(day);
    handleSelectDate({ 
      year:year,
      month: month,
      day:day
    })
  }

  useEffect(()=>{
    handleSelectDate({ 
      year:year,
      month: month,
      day:day
    })
  },[year, month])

  useEffect(()=>{
    setYear(today.getFullYear());
    setMonth(today.getMonth() + 1); // JS는 0부터 시작 → +1
    setDay("");
  }, [selectedBias])

  return (
    <div>
      <div className={style["desktop-calendar-component"]}>
        <div className={style["calendar-wrapper"]}>
          {/* 헤더 */}
          <div className={style["calendar-header-wrapper"]}>
            <div className={style["month-select-button"]}onClick={handlePrevMonth}> 이전</div>
            <div className={style["calendar-header"]}>
              <span className={style["calendar-header-span"]}>
                {year}년 {month}월
              </span>
            </div>
            <div className={style["month-select-button"]}onClick={handleNextMonth}> 다음</div>
          </div>

          {/* 요일 헤더 */}
          <div className={style["weekday-wrapper"]}>
            {weekDays.map((day, idx) => (
              <WeekDayComponent key={idx} body={day} />
            ))}
          </div>

          {/* 주차별 */}
          {weeks.map((week, idx) => (
            <div key={idx} className={style["week-component"]}>
              {week.map((item, i) => (
                <DayComponent 
                key={i}
                day={item.day}
                todayEffect={todayEffect}
                body={item.body}
                dayState={day}
                trySelectDay={trySelectDay}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const WeekDayComponent = ({ body }) => {
  const [color, setColor] = useState("transparent");

  useEffect(() => {
    if (body === "일") setColor("#FFD2D2");
    else if (body === "토") setColor("#D2FFD3");
    else{
      setColor("#fff");
    }
  }, [body]);

  return (
    <div
      className={style["week-day-component"]}
      style={{ backgroundColor: color }}
    >
      <span className={style["week-day-component-span"]}>{body}</span>
    </div>
  );
};

const DayComponent = ({ day, dayState, todayEffect, body, trySelectDay}) => {
  if (!day) {
    return <div className={style["day-component"]}></div>; // 빈칸
  }

  const IsToday = todayEffect.month && todayEffect.day === day;

  return (
    <div
      className={style["day-component"]}
      style={{
        justifyContent: body ? "space-between" : "center", 
        border: IsToday? "2px solid #83b5ff" : "none",
        backgroundColor: day == dayState ? "#83b5ff" : "transparent",
        }}
      onClick={()=>trySelectDay(day)}
    >
      <span className={style["day-component-title-span"]}
        style={{fontSize: body ? "30px" : "42px"}}
      >{day}</span>
      {body && (
        <div className={style["day-component-body"]}>
          <span className={style["day-component-body-span"]}>{body}</span>
        </div>
      )}
    </div>
  );
};


export default DesktopCalender