import style from "./BiasPageDesktop.module.css";

import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';
import { FreeMode} from 'swiper/modules';
import { 
    getBiasStateStr, getStartTime, getEndTime,
    handlePreviewImage, defaultImage, ToggleSwitch,
    fetchChangeBiasIntro, fetchChangeBiasUploadMode
} from "./BiasPageFunc";
import { useEffect, useState } from "react";
import { SCHEDULE_IMAGE_URL } from "../../constant/imageUrl";
import MyPageLoading from "../LoadingPage/MypageLoading";
import { BIAS_URL, DEFAULT_BIAS_URL } from "../../constant/biasUrl";

import follow from "./icons/follow.svg";
import share from "./icons/share.svg";
import chzzkLogo from "./icons/chzzk Icon_02.png";
import soopLogo from "./icons/soop Icon_02.png";

const BiasPageDesktop = ({
    scheduleList, targetBias, weekData, prevWeek,
     nextWeek, targetSchedule, setTargetSchedule,
      fetchTryFollowBias, is_following, isValidUser
}) => {
    const [image, setImage] = useState(null);
    const [isChecked, setIsChecked] = useState(false);

    const [introduce, setIntroduce] = useState("설명글 입니다.");
    const [introduceInput, setIntroduceInput] = useState(introduce);

    useEffect(()=>{
        setIsChecked(targetBias.open_content_mode);
        setIntroduce(targetBias.introduce);
        setIntroduceInput(targetBias.introduce);
    }, [targetBias])

    const handleChecked = async (checked) => {
        const res = await fetchChangeBiasUploadMode(targetBias.bid, !isChecked);
        setIsChecked(!isChecked);
    }

    useEffect(()=>{
        const url = `${SCHEDULE_IMAGE_URL}${targetSchedule.sid}.png`;
        handlePreviewImage(url, setImage);
    }, [targetSchedule])


    const handleChangeIntroduce = async () => {
        const res = await fetchChangeBiasIntro(targetBias.bid, introduceInput);
        if (res){
            setIntroduce(introduceInput);
        }
    }

    function onChangeIntroduceInput(e) {
        setIntroduceInput(e.target.value);
    }

    return(
        <div className={style["frame"]}>
            <div className={style["inner-wrapper"]}>
            {
                targetBias.bid != "" ? (
                    <div className={style["upper-section"]}>
                        <div className={style["top-button-wrapper"]}>
                            <div className={style["try-search-button"]}
                                onClick={()=>{window.open(`https://www.youtube.com/results?search_query=${targetBias.bname}`, '_blank');}}
                            >
                                유튜브에서 검색
                            </div>
                            <div className={style["try-follow-button"]}
                                onClick={()=>{fetchTryFollowBias(targetBias.bid)}}
                            >
                            {
                                is_following ?  "팔로우 중" : "팔로우"
                            }
                            </div>
                            {
                                isValidUser && (
                                    <div className={style["bias-option-wrapper"]}>
                                        <div className={style["bias-option-text"]}>
                                            열린 일정 모드
                                        </div>
                                        <ToggleSwitch 
                                            id={"bias-option-input"}
                                            isChecked={isChecked}
                                            handleChecked={handleChecked}
                                        />
                                    </div>
                                )
                            }
                        </div>
                        <div className={style["bias-info-wrapper"]}>
                            <div className={style["bias-image-container"]}>
                                <img
                                    src={BIAS_URL + `${targetBias.bid}.png`}
                                    onError={(e) => {
                                        e.currentTarget.onerror = null; // 무한 루프 방지
                                        e.currentTarget.src = DEFAULT_BIAS_URL;
                                    }}
                                    alt="bias"
                                />
                            </div>
                            <div className={style["bias-detail-wrapper"]}>
                                <div className={style["bias-detail-container"]}>
                                    <div className={style["bias-name-wrapper"]}>
                                        <div className={style["bias-detail-title"]}>
                                            이름
                                        </div>
                                        <div className={style["bias-name"]}>
                                            {targetBias.bname}
                                        </div>
                                    </div>
                                    <div className={style["bias-platform-container"]}
                                        onClick={() => {
                                            if (targetBias.platform_url != "https://supernova.io.kr"){
                                                window.open(targetBias.platform_url, "_blank")
                                            } else{
                                                if (targetBias.platform == "치지직"){
                                                    window.open(`https://chzzk.naver.com/search?query=${targetBias.bname}`, "_blank")
                                                }else{
                                                    window.open(`https://www.sooplive.co.kr/search?szLocation=total_search&szSearchType=total&szKeyword=${targetBias.bname}&szStype=di&szActype=input_field`, "_blank")
                                                }
                                            }
                                        }}
                                    >
                                        {
                                            targetBias.platform == "치지직" ? (
                                                <img src={chzzkLogo}/>
                                            ):(
                                                <img src={soopLogo}/>
                                            )
                                        }
                                    </div>
                                </div>

                                <div className={style["bias-detail-container2"]}>
                                    <div className={style["bias-name-wrapper2"]}>
                                        <div className={style["bias-detail-title"]}>
                                            자기소개
                                        </div>
                                        {
                                            isValidUser ? (
                                                <div className={style["bias-introduce-input-wrapper"]}>
                                                    <input className={style["bias-introduce-input"]}
                                                        value={introduceInput}
                                                        onChange={(e) => {
                                                            onChangeIntroduceInput(e);
                                                        }}
                                                        placeholder={introduce}
                                                        type="text"
                                                    />
                                                    <div className={style["fetch-intro-button"]}
                                                        onClick={handleChangeIntroduce}
                                                    >
                                                        수정하기
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className={style["bias-introduce"]}>
                                                    {targetBias.introduce || "아니"}
                                                </div>
                                            )
                                        }
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                ):(
                    <div className={style["upper-section"]}>
                        <MyPageLoading/>
                    </div>
                )
            }

            <div className={style["schedule-section"]}>
                {
                    targetSchedule.sid != "" ? (
                        <div className={style["schedule-right-section"]}>
                            <div className={style["single-schedule-image"]}>
                            {
                                image != null ? (
                                    <img src={image} alt="스케줄 이미지" />
                                ) : (
                                    <img src={defaultImage} alt="스케줄 이미지" />
                                )
                            }   
                            </div>
                            <div className={style["single-schedule-detail-wrapper"]}>
                                <div className={style["single-schedule-detail-sub-wrapper"]}>
                                    <div className={style["single-schedule-data-wrapper-left"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            제목
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            {targetSchedule.title}
                                        </div>
                                    </div>
                                    <div className={style["single-schedule-data-wrapper-right"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            스트리밍 시작 시간
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            {
                                                getStartTime(targetSchedule.datetime)
                                            }
                                        </div>
                                    </div>
                                </div>
                                <div className={style["single-schedule-detail-sub-wrapper"]}>
                                    <div className={style["single-schedule-data-wrapper-left"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            태그
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            <div className={style["tag-wrapper"]}>
                                            {
                                                targetSchedule.tags.map((tag, index)=>{
                                                    return(
                                                        <div
                                                        className={style["tag"]}
                                                        key={`tag ${index}`}
                                                        >
                                                            {tag}
                                                        </div>
                                                    );
                                                })
                                            }
                                            </div>
                                        </div>
                                    </div>
                                    <div className={style["single-schedule-data-wrapper-right"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            스트리밍 예상 종료 시각
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            {
                                                getEndTime(targetSchedule.datetime, targetSchedule.duration)
                                            }
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ):(
                        <div className={style["schedule-right-section"]}>
                            <div className={style["single-schedule-image"]}>
                                <img src={defaultImage} alt="스케줄 이미지" />
                            </div>
                            <div className={style["single-schedule-detail-wrapper"]}>
                                <div className={style["single-schedule-detail-sub-wrapper"]}>
                                    <div className={style["single-schedule-data-wrapper-left"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            제목
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            콘텐츠가 없습니다.
                                        </div>
                                    </div>
                                    <div className={style["single-schedule-data-wrapper-right"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            스트리밍 시작 시간
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            비었습니다.
                                        </div>
                                    </div>
                                </div>
                                <div className={style["single-schedule-detail-sub-wrapper"]}>
                                    <div className={style["single-schedule-data-wrapper-left"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            태그
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            태그가 없습니다.
                                        </div>
                                    </div>
                                    <div className={style["single-schedule-data-wrapper-right"]}>
                                        <div className={style["single-schedule-data-title"]}>
                                            스트리밍 예상 종료 시각
                                        </div>
                                        <div className={style["single-schedule-data-body"]}>
                                            비었습니다.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                }
                <div className={style["schedule-left-section"]}>
                    <div className={style["week-data-container"]}>
                        <div className={style["week-data"]}>
                            {`${weekData} 콘텐츠`}
                        </div>
                        <div className={style["week-button-wrapper"]}>
                            <div className={style["week-button"]}
                                onClick={prevWeek}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                    <rect x="0.5" y="0.5" width="21" height="21" rx="10.5" fill="white"/>
                                    <rect x="0.5" y="0.5" width="21" height="21" rx="10.5" stroke="#DBDBDB"/>
                                    <path d="M14 5L7.06667 10.2C6.53333 10.6 6.53333 11.4 7.06667 11.8L14 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                                </svg>
                            </div>
                            <div className={style["week-button"]}
                                onClick={nextWeek}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                    <rect x="-0.5" y="0.5" width="21" height="21" rx="10.5" transform="matrix(-1 0 0 1 21 0)" fill="white"/>
                                    <rect x="-0.5" y="0.5" width="21" height="21" rx="10.5" transform="matrix(-1 0 0 1 21 0)" stroke="#DBDBDB"/>
                                    <path d="M8 5L14.9333 10.2C15.4667 10.6 15.4667 11.4 14.9333 11.8L8 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div className={style["schedule-list-wrapper"]}>
                        <Swiper
                            slidesPerView={"auto"}
                            spaceBetween={10}
                            modules={[FreeMode]}
                            direction={"vertical"}
                            observer={true}         // ← DOM 변경 감지
                            observeParents={true}
                        >
                            {scheduleList.map((scheduleData, index) => (
                                <SwiperSlide
                                    key={index}
                                    style={{ width: "380px", height: "fit-content"}}
                                >
                                    <ScheduleComponent
                                        scheduleData={scheduleData}
                                        setTargetSchedule={setTargetSchedule}
                                    />
                                </SwiperSlide>
                            ))}
                        </Swiper>
                    </div>
                </div>
            </div>

            <div style={{height: "100px"}}>

            </div>
        </div>
    </div>
    );
}


const ScheduleComponent = ({
    scheduleData, setTargetSchedule
}) => {

    if(scheduleData.schedule.sid == ""){
        return(
            <EmptyScheduleComponent scheduleData={scheduleData}/>
        );
    }else{
        return(
            <div className={style["schedule-component"]}
                onClick={()=>{
                    setTargetSchedule(scheduleData.schedule)
                }}
            >
                <div className={style["schedule-date-wrapper"]}>
                    <div className={style["schedule-date"]}>
                        {scheduleData.date}
                    </div>
                    <div className={style["schedule-weekday"]}>
                        {scheduleData.weekday}
                    </div>
                </div>
                <div className={style["schedule-detail-wrapper"]}>
                    <div className={style["schedule-title"]}>
                        {scheduleData.schedule.title}
                    </div>
                    <div className={style["schedule-start"]}>
                        {
                            getStartTime(scheduleData.schedule.datetime)
                        }
                    </div>
                </div>
                <div className={style["tag-wrapper"]}>
                {
                    scheduleData.schedule.tags
                    .slice(0, 3)
                    .map((tag, index) => (
                        <div
                        className={style["tag"]}
                        key={`tag-${index}`}
                        >
                        {tag}
                        </div>
                    ))
                }
                </div>
            </div>
        );
    }
}

const EmptyScheduleComponent = ({
    scheduleData
})=> {
    return(
        <div className={style["schedule-component"]}
            style={{minHeight:"117px"}}
        >
            <div className={style["schedule-date-wrapper"]}>
                <div className={style["schedule-date"]}>
                    {scheduleData.date}
                </div>
                <div className={style["schedule-weekday"]}>
                    {scheduleData.weekday}
                </div>
            </div>
            <div className={style["schedule-detail-empty-wrapper"]}>
                <div className={style["schedule-title"]}>
                    {"휴방 / 미지정"}
                </div>
            </div>
            <div className={style["tag-wrapper"]}>
            </div>
        </div>
    );
}

export default BiasPageDesktop;
