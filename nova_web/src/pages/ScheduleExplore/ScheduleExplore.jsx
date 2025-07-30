import React, { useEffect, useState, useRef } from "react";
import style from "./ScheduleExplore.module.css"
import NoneSchedule from "../../component/NoneFeed/NoneSchedule";

export default function ScheduleExploreDesktop({
    setCategory, activeIndex, setActiveIndex,
    scheduleData
}) {
    const scheduleKind = ["게임", "저챗", "음악", "그림", "스포츠", "시참"];

    const handleClickCategory = (index) => {
        setActiveIndex(index);
        setCategory(scheduleKind[index]);
    }

    return(     
        <div className={style["explore_schedule_main_frame"]}>
            <div className={style["explore_schedule_container"]}>
                <div className={style["item_selcet_wrapper"]}>
                    {
                        scheduleKind.map((item, index) => {
                            const isSelected = activeIndex === index;

                            return (
                                <div
                                    className={style["category_item"]}
                                    style={{
                                        width: isSelected ? "160px" : "120px",
                                        border: isSelected ? "2px solid transparent" : "2px solid #D8E9FF",
                                        backgroundImage: isSelected 
                                            ? "linear-gradient(#fff, #fff), linear-gradient(135deg, #FFE9E9 -0.5%, #91FF94 25.38%, #8981FF 83.1%)" 
                                            : "none",
                                        backgroundOrigin: isSelected ? "border-box" : "initial",
                                        backgroundClip: isSelected ? "content-box, border-box" : "initial"
                                    }}
                                    onClick={() => handleClickCategory(index)}
                                >
                                    {item}
                                </div>
                            );
                        })
                    }
                </div>
                <div className={style["none_schedule_frame"]}>
                    {scheduleData.length === 0 && <NoneSchedule/>}
                </div>
                {
                    scheduleData.map((schedule)=>{
                        return(
                            <ScheduleComponent/>
                        );
                    })
                }
            </div>
        </div>
      
    )
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
    <div className={style["schedule_grid"]}>
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
    </div>

    );

  }

