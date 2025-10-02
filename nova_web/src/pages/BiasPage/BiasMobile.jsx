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

const BiasPageMobile = ({
    scheduleList, targetBias, weekData, prevWeek, nextWeek
}) => {

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
            <div className={style["top-bar"]}>
                <Header/>
            </div>
            <div className={style["link-ad-wrapper"]}>
                <AdComponent type={"none"}/>
            </div>
            <div className={style["inner-box"]}>
                <div className={style["bias-meta-data-wrapper"]}>
                    <div className={style["bias-image-wrapper"]}>
                        <img src={"https://kr.object.ncloudstorage.com/nova-images/ham.png"}/>
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
                        <div className={style["bias-platform-container"]}>
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
                        <div className={style["bias-meta-data-button-container"]}>
                            <div className={style["bias-meta-data-left-button"]}>외부 검색</div>
                            <div className={style["bias-meta-data-right-button"]}>팔로우</div>
                        </div>
                    </div>
                </div>

                <div className={style["week-select-box"]}>
                    <div className={style["week-data"]}>{`${weekData} 콘텐츠`}</div>
                    <div className={style["week-select-button-wrapper"]}>
                        <div className={style["prev-button"]}
                            onClick={prevWeek}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" fill="white"/>
                                <path d="M14 5L7.06667 10.2C6.53333 10.6 6.53333 11.4 7.06667 11.8L14 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>
                        <div className={style["next-button"]}
                            onClick={prevWeek}
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
                                    <ScheduleComponent schedule={schedule.schedule} />
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
                    <img src={background}/>
                </div>
            </div>
            <div style={{height:"100px"}}>

            </div>
        </div>
    );
}

const ScheduleComponent = (schedule) => {
    const [image, setImage] = useState(null);

    useEffect(()=>{
        const url = `${SCHEDULE_IMAGE_URL}${schedule.sid}.png`;
        handlePreviewImage(url, setImage);
    }, [])

    return(
        <div className={style["single-schedule-container"]}>
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
                <div className={style["single-schedule-title"]}>
                    {schedule.schedule.title || "콘텐츠 없음"}
                </div>
                <div className={style["single-start-time"]}>
                    {
                        getStartTime(schedule.schedule.datetime)
                    }
                </div>
                <div className={style["schedule-tag-wrapper"]}>
                    {schedule.schedule.tags.length > 0 ? (
                        schedule.schedule.tags.map((tag, tIdx) => (
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