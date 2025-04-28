import React, { useEffect, useState } from "react";
import style from "./time_layer_box.module.css";
import component_style from "./schedule_component.module.css";
import right_vector_arrow from "./../../../img/right-vector-arrow.svg";
import background_gradient from "./../../../img/background_gradient.svg";
import calender_icon from "./../../../img/calender.svg";
import shop_icon from "./../../../img/3d_shop_icon.png";


export default function TimeLayerBox({scheduleData, formattedDate}) {
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

    return (
        <div className={style["time-layer-box"]}>
            <div className={style["time-layer-info"]}>
                <div className={style["tag-box"]}>
                    <img src={shop_icon}/>
                    <span>
                        {scheduleData[0].tag}
                    </span>
                </div>
                <div className={style["calender-box"]}>
                    <img src={calender_icon}/>
                    <span>
                        {formattedDate}
                    </span>
                </div>
                
            </div>
            <div>
                {scheduleData.slice(1, visibleCount).map((item, index) => (
                    <ScheduleComponent key={index} section={item.section} schedules={item.schedules} />
                ))}
            </div>
           <img src={background_gradient} alt="gradient" className={style["background-gradient"]} 
            style={{ opacity, transition: "opacity 1s" }} />
        </div>
    );
}

function ScheduleComponent({ section, schedules}) {
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

    if (schedules.length === 1) {
        return (
            <div className={component_style["schedule-component"]}
            style={transitionStyle}
            >
                <div className={component_style["schedule-section-box"]}>
                    <span className={component_style["schedule-section"]}>
                        {section}
                    </span>
                </div>
                <div className={component_style["outer-schedule-box"]}>
                <ScheduleDetail {...schedules[0]}/>
                </div>
            </div>
        );
    } else if (schedules.length > 1) {
        return (
            <div className={component_style["schedule-component"]}
            style={transitionStyle}
            >
                <div className={component_style["schedule-section-box"]}>
                    <span className={component_style["schedule-section"]}>
                        {section}
                    </span>
                </div>
                <div className={component_style["outer-schedule-box"]}>
                {
                    schedules.map((schedule, index) => {
                        return (
                            <div>
                                <ScheduleDetail key= {index} {...schedule}/>
                                {index % 2 === 0 && (
                                    <div className={component_style["schedule-sperator"]}></div>
                                )}
                            </div>
                        )
                    })
                }
                </div>
            </div>
        );
    }else{
        return (
            <div className={component_style["schedule-component"]}
            style={transitionStyle}
            >
                <div className={component_style["schedule-section-box"]}>
                    <span className={component_style["schedule-section"]}>
                        {section}
                    </span>
                </div>
                <span className={component_style["empty-schedule-span"]}>
                    이 시간은 조용하군요
                </span>
            </div>
        );
    }
}


function ScheduleDetail({ time, type, schedule_id, schedule_title, schedule_bias}) {
    const [isClicked, setIsClicked] = useState(false); // 클릭 여부를 관리하는 상태

    const handleClick = () => {
        setIsClicked(true); // 클릭 시 색상을 변경
        setTimeout(() => {
            setIsClicked(false); // 1초 후 원래 상태로 돌아가게 설정
        }, 1000); // 1000ms = 1초 후 원래 색으로 돌아가도록 설정
    };

    return (
        <div className={component_style["schedule-detail-box"]}
            onClick={handleClick} // 클릭 시 색상 변경
            style={{
                backgroundColor: isClicked ? "rgba(255,255,255,0.7)" : "", // 클릭 시 배경색 변경
                transition: "background-color 0.3s ease", // 부드러운 색상 전환
            }}
        >
            <span className={component_style["time-span"]}>
                {time}
            </span>
            <ScheduleExposeType type={type}/>
            <div className={component_style["schedule-detail"]}>
                <div className={component_style["schedule-title"]}>
                    {schedule_title}
                </div>
                <div className={component_style["schedule-bias"]}>
                    {schedule_bias}
                </div>  
            </div>
            <div className={component_style["schedule-arrow"]}>
                <img src={right_vector_arrow} />
            </div>
        </div>
    );
}

function ScheduleExposeType( {type} ){

    if(type === "recommened"){
        return (
            <div className={component_style["recommened-schedule"]}>
                추천
            </div>
        );
    }
    else{
        return (
            <div className={component_style["added-schedule"]}>
                구독
            </div>
        );
    }
}