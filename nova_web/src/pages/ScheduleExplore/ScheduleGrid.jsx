import style from "./ScheduleExplore.module.css"
import { useState } from "react";
import { formatDateTime, fecthSubScribeSchedule } from "./ScheduleComponentFunc";
import { fetchSubscribeSchedule } from "./ScheduleComponentFunc";

export default function ScheduleGrid({ scheduleData, toggleDetailOption }) {
  return (
    <div className={style["schedule_grid"]}>
      {scheduleData.map((schedule) => (
        <ScheduleComponent key={schedule.code} toggleDetailOption={toggleDetailOption} {...schedule} />
      ))}   
      </div>
  );
}

function ScheduleComponent({
    toggleDetailOption,
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
                isClicked ? (
                    <div className={style["schedule_extra_control_container"]}>
                        <div className={style["schedule_detail"]}
                          onClick={()=>{toggleDetailOption(sid)}}
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
                ):(
                  <div 
                    style={{height: "68px"}}
                  >
                  </div>
                )
            }
        </div>
    );
  }
