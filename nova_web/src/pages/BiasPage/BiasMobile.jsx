import { motion, AnimatePresence} from "framer-motion";
import style from "./BiasPage.module.css";
import Header from "../../component/Header/Header";
import background from "./background.svg";
import AdComponent from "../../component/AdComponent/AdComponent";
import chzzkLogo from './chzzklogo_kor(Green).svg';
import soopLogo from './SOOP_LOGO_Blue 1.png';
import { getBiasStateStr, getStartTime, handlePreviewImage, defaultImage } from "./BiasPageFunc";
import { useEffect, useState } from "react";
import { SCHEDULE_IMAGE_URL } from "../../constant/imageUrl";
import NavBar from "../../component/NavBar/NavBar";
import { BIAS_URL, DEFAULT_BIAS_URL } from "../../constant/biasUrl";
import ScheduleDetailMobile from "../../component/ScheduleDetail/ScheduleDetailMobile";

const BiasPageMobile = ({
    scheduleList, targetBias, weekData, prevWeek, nextWeek, fetchTryFollowBias, is_following
}) => {

    const [targetSchedule, setTargetSchedule] = useState(null);
    const [showScheduleMoreOption, setShowScheduleMoreOption] = useState(false);

    const handleTargetSchedule = (schedule) => {
        setTargetSchedule(schedule.sid);
        toggleDetailOption();
    }

    const toggleDetailOption = () => {
        setShowScheduleMoreOption(!showScheduleMoreOption);
    }

    // 부모 컨테이너 애니메이션 설정
    const containerVariants = {
        hidden: {},
        visible: {
            transition: {
                staggerChildren: 0.15, // 0.15초 간격으로 순차 등장
            },
        },
    };


    // 자식(각 아이템) 애니메이션 설정
    const itemVariants = {
        hidden: { opacity: 0, y: 20 }, // 아래에서 올라옴
        visible: { opacity: 1, y: 0 }, // 원래 위치
    };

    return (
        <div className={style["frame"]}>
            {
                showScheduleMoreOption && 
                <ScheduleDetailMobile
                    sid={targetSchedule}
                    toggleDetailOption={toggleDetailOption}
                />
            }
            <div className={style["top-bar"]}>
                <Header/>
            </div>
            <div className={style["link-ad-wrapper"]}>
                <AdComponent type={"none"}/>
            </div>
            <div className={style["inner-box"]}>
                <div className={style["bias-meta-data-wrapper"]}>
                    <div className={style["bias-image-wrapper"]}>
                        <img
                            src={BIAS_URL + `${targetBias.bid}.png`}
                            onError={(e) => {
                                e.currentTarget.onerror = null; // 무한 루프 방지
                                e.currentTarget.src = DEFAULT_BIAS_URL;
                            }}
                            alt="bias"
                        />
                    </div>
                    <div className={style["bias-detail-container-wrapper"]}>
                        <div className={style["bias-name-container"]}>
                            <div className={style["bias-state"]}>
                            {
                                getBiasStateStr(targetBias.state)
                            }
                            </div>
                            <div className={style["bias-name"]}>{targetBias.bname}</div>
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
                            <div className={style["platform-image"]}>
                            {
                                targetBias.platform == "치지직" ? (
                                    <img src={chzzkLogo}/>
                                ):(
                                    <img src={soopLogo}/>
                                )

                            }
                            </div>
                            <div className={style["platform-direct-link"]}>바로가기</div>
                        </div>
                    </div>
                </div>
                <div className={style["bias-meta-data-button-container"]}>
                    <div className={style["bias-meta-data-left-button"]}
                        onClick={()=>{window.open(`https://www.youtube.com/results?search_query=${targetBias.bname}`, '_blank');}}
                    >외부 검색</div>
                    <div className={style["bias-meta-data-right-button"]}
                        onClick={()=>{fetchTryFollowBias(targetBias.bid)}}
                    >
                    {
                        is_following ?  "팔로우 중" : "팔로우"
                    }
                    </div>
                </div>

                <div className={style["week-select-box"]}>
                    <div className={style["week-select-button-wrapper"]}>
                        <div className={style["prev-button"]}
                            onClick={prevWeek}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" fill="white"/>
                                <path d="M14 5L7.06667 10.2C6.53333 10.6 6.53333 11.4 7.06667 11.8L14 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>

                        <div className={style["week-data"]}>{`${weekData} 콘텐츠`}</div>

                        <div className={style["next-button"]}
                            onClick={nextWeek}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" transform="matrix(-1 0 0 1 22 0)" fill="white"/>
                                <path d="M8 5L14.9333 10.2C15.4667 10.6 15.4667 11.4 14.9333 11.8L8 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>
                    </div>
                </div>
                <motion.div
                    className={style["schedule-list-wrapper"]}
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                    key={scheduleList.map(s => s.schedule.sid || s.date).join("-")} 
                    // scheduleList가 바뀌면 key가 바뀌어 animate 재실행
                >
                    <AnimatePresence>
                        {scheduleList.map(schedule => (
                            <motion.div
                                key={schedule.schedule.sid || schedule.date} // 고유 key
                                className={style["single-schedule-wrapper"]}
                                variants={itemVariants}
                                initial="hidden"
                                animate="visible"
                                exit={{ opacity: 0, y: 20 }}
                                transition={{ duration: 0.5, ease: "easeOut" }}
                            >
                                <div className={style["schedule-datetime-wrapper"]}>
                                    <div className={style["schedule-datetime"]}>
                                        {schedule.date || "날짜 없음"}
                                    </div>
                                    <div className={style["datetime-weekday"]}>
                                        {schedule.weekday || ""}
                                    </div>
                                </div>

                                {schedule.schedule.sid !== "" ? (
                                    <ScheduleComponent schedule={schedule.schedule} handleTargetSchedule={handleTargetSchedule} />
                                ) : (
                                    <div className={style["single-schedule-container"]}>
                                        <div className={style["single-schedule-image"]}>
                                            <img src={"https://kr.object.ncloudstorage.com/nova-images/no-image.png"} />
                                        </div>
                                        <div className={style["empty-schedule"]}>휴방 / 미지정</div>
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </motion.div>

                <div className={style["background-gradient"]}>
                </div>
            </div>
            <div style={{height:"100px"}}> </div>
            <NavBar />
        </div>
    );
}

const ScheduleComponent = ({schedule, handleTargetSchedule}) => {
    const [image, setImage] = useState(null);

    useEffect(()=>{
        const url = `${SCHEDULE_IMAGE_URL}${schedule.sid}.png`;
        handlePreviewImage(url, setImage);
    }, [])

    return(
        <div className={style["single-schedule-container"]}
            onClick={()=>{handleTargetSchedule(schedule)}}
        >
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
                <div className={style["single-schedule-title-wrapper"]}>
                    <div className={style["single-schedule-title"]}>
                        {schedule.title || "콘텐츠 없음"}
                    </div>
                    <div className={style["single-start-time"]}>
                        {
                            getStartTime(schedule.datetime)
                        }
                    </div>
                </div>
                <div className={style["schedule-tag-wrapper"]}>
                    {schedule.tags.length > 0 ? (
                        schedule.tags.slice(0, 3).map((tag, tIdx) => (
                            <div key={tIdx} className={style["tag"]}>
                                {tag}
                            </div>
                        ))
                    ) : (
                        <div className={style["tag"]}>-</div>
                    )}
                </div>
            </div>
        </div>
    );
}


export default BiasPageMobile;