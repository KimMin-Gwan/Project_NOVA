import { useState } from "react";
import style from "./ScheduleComponentMobile.module.css";
import { formatDateTime, fecthSubScribeSchedule} from "./ScheduleComponentFunc";


const ScheduleComponentMobile = ({
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
}) => {

    const { formattedDate, formattedTime } = formatDateTime(datetime);
    const [isClicked, setIsClicked] = useState(false);
    const [isSubscribe, setIsSubscribe] = useState(subscribe);

    return (
        <div className={style["schedule-component-wrapper"]}>
            <div className={style["schedule-component-frame"]}
              onClick={()=>{setIsClicked(!isClicked)}}
              style={{borderRadius : isClicked ? "12px 12px 0px 0px" : "12px 12px 12px 12px"}}
            >
                <div className={style["schedule-component-detail-wrapper"]}>
                    <div className={style["schedule-component-detail"]}>
                        <div className={style["schedule-title"]}> {title} </div>
                        <div className={style["schedule-bname"]}> {bname} </div>
                        <div className={style["schedule-datetime-wrapper"]}>
                            <div className={style["schedule-datetime"]}>
                                {formattedDate} | {formattedTime}
                            </div>
                        </div>
                    </div>
                    <div className={style["schedule-platform"]}> {platform} </div>
                </div>
            </div>
            {
                isClicked && 
                <div className={style["schedule-button-wrapper"]}>
                    <div className={style["schedule-button-left"]}
                        onClick={()=>{toggleDetailOption(sid)}}
                    >
                        자세히
                    </div>
                    {
                        isSubscribe ? 
                        <div className={style["schedule-button-right"]}
                            onClick={()=>{
                              if (fecthSubScribeSchedule(sid)){
                                setIsSubscribe(!isSubscribe)
                              }}}
                        >
                            구독취소
                        </div>
                        :
                        <div className={style["schedule-button-right"]}
                            onClick={()=>{
                              if (fecthSubScribeSchedule(sid)){
                                setIsSubscribe(!isSubscribe)
                              }
                            }}
                        >
                            구독하기
                        </div>
                    }
                </div>
            }
        </div>
    );
}

export default ScheduleComponentMobile