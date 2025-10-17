import React, { useRef, useEffect, useState } from "react";
import style from "./ScheduleDetailMobile.module.css";
import { handlePreviewImage, formatKoreanDateTime, fetchScheduleData, fetchSubscribeSchedule } from "./ScheduleDetailFunction";
import { SCHEDULE_IMAGE_URL } from "../../constant/imageUrl";
import { useLocation, useNavigate } from "react-router-dom";
import MyPageLoading from "../../pages/LoadingPage/MypageLoading";

const ScheduleDetailMobile = ({sid, toggleDetailOption}) => {
    const defaultImage= "https://kr.object.ncloudstorage.com/nova-images/no-image.png";
    const [image, setImage] = useState(null);
    const [tags, setTags] = useState([]);
    const [schedule, setSchedule] = useState({});
    const [subscribe, setSubscribe] = useState(true);
    const [isLoading, setIsLoading] = useState(true);
    const datetime = new Date(schedule.datetime);
    const location = useLocation();

    const navigate = useNavigate();
    
    useEffect(()=>{
        const fetchData = async () => {
            try {
                const schedule = await fetchScheduleData(sid); // ✅ 데이터 기다림
                if (!schedule || !schedule.sid) {
                    alert("콘텐츠 일정을 불러오는데 문제가 있습니다.");
                    toggleDetailOption(false);
                    return;
                }
                
                setSchedule(schedule);
                setTags(schedule.tags);
                setSubscribe(schedule.subscribe);

                const url = `${SCHEDULE_IMAGE_URL}${schedule.sid}.png`;
                handlePreviewImage(url, setImage);
                setIsLoading(false);
            } catch (error) {
                console.error("일정 불러오기 실패:", error);
                alert("일정을 불러오는 중 오류가 발생했습니다.");
                toggleDetailOption(false);
            }
        };

        fetchData();
    },[])

    const { dateStr, timeStr } = formatKoreanDateTime(datetime);

    if (isLoading){
        <div className={style["modal-frame"]}
            onClick={()=>{toggleDetailOption(false);}}
        >
            <div className={style["modal-container"]}>
                <MyPageLoading/>
            </div>
        </div>
    }else{
        return(
            <div className={style["modal-frame"]}
                onClick={()=>{toggleDetailOption(false);}}
            >
                <div className={style["modal-container"]}
                    onClick={(e) => e.stopPropagation()}
                >
                    {
                        isLoading ?  <MyPageLoading/> 
                        :
                        <>
                            <div className={style["modal-upper-section"]}>
                                <div className={style["schedule-image-wrapper"]}
                                    onClick={()=>{
                                        toggleDetailOption(null);
                                        navigate(`/bias/${schedule.bid}`);
                                    }}
                                >
                                    <div className={style["schedule-image"]}>
                                        <img src={image ?? defaultImage} alt="스케줄 이미지" />
                                    </div>
                                    <div className={style["schedule-bias-hyper-link"]}>
                                        이미지를 눌러 스트리머 페이지로 이동
                                    </div>
                                </div>
                            </div>
                            <div className={style["modal-lower-section"]}>
                                <div className={style["schedule-tag-detail-wrapper"]}>
                                    <div className={style["tag-wrapper-wrapper"]}>
                                        <div className={style["tag-wrapper"]}>
                                            {
                                                tags.map((tag, i)=>{
                                                    return(
                                                        <div
                                                        key={i}
                                                         className={style["tag-box"]}
                                                         >
                                                            {tag}
                                                        </div>
                                                    )
                                                })
                                            }
                                            {
                                                schedule.platform &&
                                                <div className={style["platform-box"]}>
                                                    {schedule.platform}
                                                </div>
                                            }
                                        </div>
                                        <div className={style["schedule-bname"]}
                                            onClick={()=>{
                                                navigate(`/bias/${schedule.bid}`);
                                                toggleDetailOption(null);
                                            }}
                                        >
                                            {schedule.bname}
                                        </div>
                                    </div>
                                    <div className={style["schedule-detail-wrapper"]}>
                                        <div className={style["schedule-title"]}>
                                            {schedule.title}
                                        </div>
                                        <div className={style["schedule-datetime"]}>
                                            <div>
                                                {dateStr}
                                            </div>
                                            <div>
                                                |
                                            </div>
                                            <div>
                                                {timeStr}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className={style["button-wrapper"]}>
                                    {
                                        subscribe ? (
                                            <div className={style["left-button-wrapper"]}>
                                                <div className={style["left-button2"]}
                                                    onClick={() => {
                                                        if (schedule.url != "https://supernova.io.kr"){
                                                            window.open(schedule.url, "_blank")
                                                        } else{
                                                            if (schedule.platform == "치지직"){
                                                                window.open(`https://chzzk.naver.com/search?query=${schedule.bname}`, "_blank")
                                                            }else{
                                                                window.open(`https://www.sooplive.co.kr/search?szLocation=total_search&szSearchType=total&szKeyword=${schedule.bname}&szStype=di&szActype=input_field`, "_blank")
                                                            }
                                                        }
                                                    }}
                                                >
                                                    플랫폼 바로가기
                                                </div>
                                                <span className={style["left-span-button"]}
                                                    onClick={() => {
                                                        navigate(`/write_feed?title=${schedule.title}&bias=${schedule.bid}&biasName=${schedule.bname}`)
                                                    }}
                                                >
                                                    태그하고 글쓰기
                                                </span>
                                            </div>
                                        ):(
                                            <div className={style["left-button"]}
                                                onClick={() => {
                                                    if (schedule.url != "https://supernova.io.kr"){
                                                        window.open(schedule.url, "_blank")
                                                    } else{
                                                        if (schedule.platform == "치지직"){
                                                            window.open(`https://chzzk.naver.com/search?query=${schedule.bname}`, "_blank")
                                                        }else{
                                                            window.open(`https://www.sooplive.co.kr/search?szLocation=total_search&szSearchType=total&szKeyword=${schedule.bname}&szStype=di&szActype=input_field`, "_blank")
                                                        }
                                                    }
                                                }}
                                            >
                                                플랫폼 바로가기
                                            </div>
                                        )
                                    }{
                                        schedule.is_owner ? (
                                            <div className={style["right-button"]}
                                                onClick={()=>{
                                                    navigate(`/schedule/make_new/${schedule.sid}`)
                                                }}
                                            >콘텐츠 수정</div>
                                        ) : (
                                            subscribe ? (
                                            <div className={style["right-button"]}
                                                onClick={async () => {
                                                    const ok = await fetchSubscribeSchedule(schedule.sid, setSubscribe);
                                                    if (!ok) {
                                                        if (window.confirm("로그인이 필요합니다. 로그인 페이지로 이동할까요?")) {
                                                            navigate("/novalogin", { state: { from: location.pathname } }); 
                                                        }
                                                    }
                                                }}
                                            >구독 취소</div>
                                            ) : (
                                            <div className={style["right-button"]}
                                                onClick={async () => {
                                                    const ok = await fetchSubscribeSchedule(schedule.sid, setSubscribe);
                                                    if (!ok) {
                                                        if (window.confirm("로그인이 필요합니다. 로그인 페이지로 이동할까요?")) {
                                                            navigate("/novalogin", { state: { from: location.pathname } }); 
                                                        }
                                                    }
                                                }}
                                            >콘텐츠 구독</div>
                                            )
                                        )
                                    }
                                </div>
                            </div>
                        </>
                    }
                </div>
            </div>
        );
    }
}


export default ScheduleDetailMobile;
