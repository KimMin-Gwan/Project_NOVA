import style from "./ScheduleExplore.module.css"
import { useState } from "react";
import { formatDateTime, fetchSubScribeSchedule } from "./ScheduleComponentFunc";
import { fetchSubscribeSchedule } from "./ScheduleComponentFunc";
import { useLocation, useNavigate } from "react-router-dom";

export default function ScheduleGrid({ scheduleData, toggleDetailOption }) {
  const navigate = useNavigate()
  return (
    <div className={style["schedule_grid"]}>
      {scheduleData.map((schedule) => (
        <ScheduleComponent 
          key={schedule.code}
          toggleDetailOption={toggleDetailOption} 
          navigate={navigate}
          {...schedule} />
      ))}   
      </div>
  );
}

function ScheduleComponent({
    toggleDetailOption,
    navigate,
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
    const location = useLocation();
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
                            onClick={async () => {
                                const ok = await fetchSubscribeSchedule(sid, setIsSubscribe);
                                if (!ok) {
                                    if (window.confirm("로그인이 필요합니다. 로그인 페이지로 이동할까요?")) {
                                        navigate("/novalogin", { state: { from: location.pathname } });
                                    }
                                }
                            }}
                          >구독취소</div>
                          : <div className={style["schedule_subscribe"]}
                              onClick={async () => {
                                  const ok = await fetchSubscribeSchedule(sid, setIsSubscribe);
                                  if (!ok) {
                                      if (window.confirm("로그인이 필요합니다. 로그인 페이지로 이동할까요?")) {
                                          navigate("/novalogin", { state: { from: location.pathname } });
                                      }
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
