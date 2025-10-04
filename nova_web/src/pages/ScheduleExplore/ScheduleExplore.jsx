import style from "./ScheduleExplore.module.css"
import NoneSchedule from "../../component/NoneFeed/NoneSchedule";
import ScheduleGrid from "./ScheduleGrid.jsx";
import { useState } from "react";
import ScheduleDetailDekstop from "../../component/ScheduleDetail/ScheduleDetailDesktop.jsx";
import AdComponent from "../../component/AdComponent/AdComponent.jsx";

export default function ScheduleExploreDesktop({
    setCategory, activeIndex, setActiveIndex,
    scheduleData, setKey, fetchMoreSearchData
}) {
    const scheduleKind = ["게임", "저챗", "음악", "그림", "스포츠", "시참"];

    const handleClickCategory = (index) => {
        setKey(-1);
        setActiveIndex(index);
        setCategory(scheduleKind[index]);
    }

    const [showScheduleMoreOption, setShowScheduleMoreOption] = useState(false);
    const [targetSchedule, setTargetSchedule] = useState("");

    const toggleDetailOption = (targetSchedule) => {
        setTargetSchedule(targetSchedule);
        setShowScheduleMoreOption(!showScheduleMoreOption);
    }

    const handleFetchMoreSearchData = async () =>{
        const result = await fetchMoreSearchData();
        if (!result){
            alert("더 불러올 콘텐츠가 없습니다.");
        }
    }


    return(     
        <div className={style["explore_schedule_main_frame"]}>
            {
                showScheduleMoreOption && 
                <ScheduleDetailDekstop
                    sid={targetSchedule}
                    toggleDetailOption={toggleDetailOption}
                />
            }
            <div className={style["explore_schedule_container"]}>
                <AdComponent type={"link"}/>
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
                {scheduleData.length === 0 && 
                    <div className={style["none_schedule_frame"]}>
                        <NoneSchedule/>
                    </div>
                }
                <ScheduleGrid scheduleData={scheduleData} toggleDetailOption={toggleDetailOption} />
                <div className={style["fetch-more-button-wrapper"]}>
                    <div className={style["fetch-more-button"]}
                        onClick={()=>{
                            handleFetchMoreSearchData()
                        }}
                    >
                        더 불러오기
                    </div>
                </div>
            </div>
            <div className={style["desktop-ad-section-style"]}>
                <AdComponent type={"image_32x60"}/>
            </div>
        </div>
    )
  }



