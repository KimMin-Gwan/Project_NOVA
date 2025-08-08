import style from "./ScheduleExplore.module.css"
import { useState } from "react";

export default function ScheduleGrid({ scheduleData }) {
  return (
    <div className={style["schedule_grid"]}>
      {scheduleData.map((schedule) => (
        <ScheduleComponent key={schedule.code} {...schedule} />
      ))}   
      </div>
  );
}

function ScheduleComponent({
    detail,
    uname,
    update_time,
    bname,
    start_date,
    start_time,
    location,
    code,
    toggleClick,
    selectBack,
  }){

    const [isClicked, setIsClicked] = useState(false);

    return(
        <div className={style["schedule_component_wrapper"]}>
            <div className={style["schedule_wrapper"]}>
                <span className={style["schedule_title"]}>{detail}</span>
                <div className={style["schedule_detail_container"]}>
                    <span className={style["artist_name"]}>{bname}</span>
                    <div className={style["schedule_time_wrapper"]}>
                        <span className={style["schedule_time"]}>{start_date} | {start_time}</span>
                    </div>
                    <span className={style["schedule_platform"]}>{location}</span>
                </div>
            </div>
            {
                isClicked && (
                    <div className={style["schedule_extra_control_container"]}>
                        <div className={style["schedule_detail"]}>자세히</div>
                        <div className={style["schedule_subscribe"]}>구독하기</div>
                    </div>
                )
            }
        </div>
    );
  }