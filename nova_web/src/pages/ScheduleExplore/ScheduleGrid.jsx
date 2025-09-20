import style from "./ScheduleExplore.module.css"
import { useState } from "react";
import mainApi from "../../services/apis/mainApi";

export default function ScheduleGrid({ scheduleData, toggleMoreOption }) {
  return (
    <div className={style["schedule_grid"]}>
      {scheduleData.map((schedule) => (
        <ScheduleComponent key={schedule.code} toggleMoreOption={toggleMoreOption} {...schedule} />
      ))}   
      </div>
  );
}

function ScheduleComponent({
    toggleMoreOption,
    title,
    sid,
    uname,
    update_time,
    bname,
    datetime,
    platform,
    code,
    toggleClick,
    selectBack,
    subscribe
  }){

    const [isClicked, setIsClicked] = useState(false);
    const { formattedDate, formattedTime } = formatDateTime(datetime);
    const [isSubscribe, setIsSubscribe] = useState(subscribe);

    return(
        <div className={style["schedule_component_wrapper"]}>
            <div className={style["schedule_wrapper"]}
              onClick={()=>{setIsClicked(!isClicked)}} >
                <span className={style["schedule_title"]}>{title}</span>
                <div className={style["schedule_detail_container"]}>
                    <span className={style["artist_name"]}>{bname}</span>
                    <div className={style["schedule_time_wrapper"]}>
                      <span className={style["schedule_time"]}>
                        {formattedDate} | {formattedTime}
                      </span>
                    </div>
                    <span className={style["schedule_platform"]}>{platform}</span>
                </div>
            </div>
            {
                isClicked && (
                    <div className={style["schedule_extra_control_container"]}>
                        <div className={style["schedule_detail"]}
                          onClick={()=>{toggleMoreOption(sid)}}
                        >자세히</div>
                        {
                          isSubscribe? <div className={style["schedule_subscribe"]}
                            onClick={()=>{
                              if (fecthSubScribeSchedule(sid)){
                                setIsSubscribe(!isSubscribe)
                              }
                            }}
                          >구독취소</div>
                          : <div className={style["schedule_subscribe"]}
                            onClick={()=>{
                              if (fecthSubScribeSchedule(sid)){
                                setIsSubscribe(!isSubscribe)
                              }
                            }}
                          >구독하기</div>
                        }
                    </div>
                )
            }
        </div>
    );
  }

function formatDateTime(dateStr) {
  const date = new Date(dateStr);

  // 날짜
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  // 요일
  const weekDays = ["일", "월", "화", "수", "목", "금", "토"];
  const week = weekDays[date.getDay()];

  const formattedDate = `${month}월 ${day}일 ${week}`;

  // 시간
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const ampm = hours >= 12 ? "오후" : "오전";
  hours = hours % 12;
  hours = hours ? hours : 12; // 0 -> 12
  const formattedTime = `${ampm} ${String(hours).padStart(2,"0")}:${minutes}`;

  return { formattedDate, formattedTime };
}

const fecthSubScribeSchedule = (sid) => {
  mainApi.get(`/time_table_server/try_subscribe_schedule?sid=${sid}`).then((res)=>{
    const body = res.data.body;
  })
  return true
}