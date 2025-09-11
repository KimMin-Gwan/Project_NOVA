import React, { act, useEffect, useState, useRef } from "react";
import time_layer_box_style from "./time_layer_box.module.css";
import component_style from "./schedule_component.module.css";
import right_vector_arrow from "./../../../img/right-vector-arrow.svg";
import background_gradient from "./../../../img/background_gradient.svg";
import calender_icon from "./../../../img/calender.svg";
import double_arrow_round from "./../../../img/double_arrow_round.svg";
import shop_icon from "./../../../img/3d_shop_icon.png";

import style from "./TimeLayerBoxDesktop.module.css";


export default function TimeLayerBoxDesktop({
    scheduleData, formattedDate, isFetching,
    onChangeIndexNext, onChangeIndexPrev, onClickSchedule
}){
    const [visibleCount, setVisibleCount] = useState(0); // 렌더링된 컴포넌트 개수
    const [opacity, setOpacity] = useState(0);

    const delay = 100; // 지연 시간 (0.5초)

    useEffect(() => {
        if (visibleCount < scheduleData.length) {
        const timer = setTimeout(() => {
            setVisibleCount((prev) => prev + 1);
        }, delay);
        return () => clearTimeout(timer); // cleanup
        }

        const timer = setTimeout(() => {
            setOpacity(1); // 애니메이션으로 나타나게 함
        }, 300); // 약간의 딜레이 추가
        return () => clearTimeout(timer); // 컴포넌트 언마운트 시 타이머 정리
    }, [visibleCount, scheduleData.length]);


    async function onClickPrevArrow() {
        await onChangeIndexPrev()
    }

    async function onClickNextArrow() {
        await onChangeIndexNext()
    }

    return(
        <div className={style["schedule-dashboard-main-container"]}>
            <div className={time_layer_box_style["time-layer-info"]} style={{display:"flex", alignContent:"center", justifyContent:"center"}}>
                <div className={time_layer_box_style["slide-arrow-box"]}>
                    <img src={double_arrow_round} style={{cursor:"pointer"}}
                    onClick={()=>{
                        if (isFetching) return;
                        onChangeIndexPrev();
                    }}
                    />
                </div>
                <div className={time_layer_box_style["calender-box-v1"]}>
                    <img src={calender_icon}/>
                    <span>
                        {formattedDate}
                    </span>
                </div>
                <div className={time_layer_box_style["slide-arrow-box"]}>
                    <img src={double_arrow_round} style={{rotate:"180deg", cursor:"pointer"}}
                    onClick={()=>{
                        if (isFetching) return;
                        onClickNextArrow()
                    }}
                    />
                </div>
            </div>
            {scheduleData.slice(1, visibleCount).map((item, index) => (
                <ScheduleComponentDesktop key={index} section={item.section} schedules={item.schedules} onClickSchedule={onClickSchedule} />
            ))}
           <img src={background_gradient} alt="gradient" className={time_layer_box_style["background-gradient"]} 
            style={{ opacity, transition: "opacity 1s" }} />
        </div>
    );
}

function ScheduleComponentDesktop({ section, schedules, onClickSchedule}){
    const [opacity, setOpacity] = useState(0);
    const [transform, setTransform] = useState("translateY(20px)"); // 처음에는 살짝 아래로 이동

    useEffect(() => {
        const timer = setTimeout(() => {
        setOpacity(1); // 애니메이션으로 나타나게 함
        setTransform("translateY(0)"); // 자연스럽게 원래 위치로 이동
        }, 100); // 약간의 딜레이 추가
        return () => clearTimeout(timer); // 컴포넌트 언마운트 시 타이머 정리
    }, []);

    const transitionStyle = {
        opacity,
        transform,
        transition: "opacity 1s, transform 1s", // 투명도와 transform을 동시에 애니메이션
    };

    return(
        <div className={style["schedule-component-wrapper"]}
            style={transitionStyle}
        >
            <div className={style["schedule-component-time-data-wrapper"]}>
                {section}
            </div>
            {
                schedules.length == 0 ? (
                    <div className={style["schedule-component"]}
                        style={{justifyContent:"center"}}
                    >
                        <span className={style["schedule-component-empty"]}>
                            이 시간은 조용하군요
                        </span>
                    </div>
                ) : (
                    schedules.map((schedule, index) => {
                        return (
                            <ScheduleDetail key= {index} {...schedule} onClickSchedule={onClickSchedule}/>
                        );
                    })
                )
            }
        </div>
    );
}



function ScheduleDetail({
    time, type, schedule_id,
    schedule_title, schedule_bias, onClickSchedule
}) {

    const handleClick = (e) => {
        onClickSchedule(schedule_id); // 꾹 누르기 동작 실행
    };

    return (
        <div className={style["schedule-component"]}
            onClick={handleClick}
        >
            <div className={style["schedule-component-left-wrapper"]}>
                <span>{formatAMPM(time)}</span>
                <ScheduleExposeType type={type} />
            </div>
            <div className={style["schedule-component-right-wrapper"]}>
                <div className={style["schedule-component-body-wrapper"]}>
                    <span className={style["schedule-component-title"]}>
                        {schedule_title}
                    </span>
                    <span className={style["schedule-component-streamer"]}>
                        {schedule_bias}
                    </span>
                </div>
                <div className={style["schedule-component-arrow"]}>
                    <img src={right_vector_arrow}/>
                </div>
            </div>
        </div>
    );
}

function ScheduleExposeType( {type} ){

    if(type === "추천"){
        return (
            <div className={style["schedule-component-recommend-outer"]}>
                <div className={style["schedule-component-state-white-background"]}>
                    <div className={style["schedule-component-recommend-inner"]}>
                        추천
                    </div>
                </div>
            </div>
        );
    }
    else{
        return (
            <div className={style["schedule-component-subscribe-outer"]}>
                <div className={style["schedule-component-state-white-background"]}>
                    <div className={style["schedule-component-subscribe-inner"]}>
                        구독
                    </div>
                </div>
            </div>
        );
    }
}


const formatAMPM = (dateStr) => {
    const date = new Date(dateStr);
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 -> 12
    const minStr = minutes.toString().padStart(2, "0");

    return `${ampm} ${hours.toString().padStart(2, "0")}:${minStr}`;
}