import { motion } from "framer-motion";
import style from "./BiasPage.module.css";
import Header from "../../component/Header/Header";
import background from "./background.svg";
import AdComponent from "../../component/AdComponent/AdComponent";

import BiasPageDesktop from "./BiasPageDesktop";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import useMediaQuery from "@mui/material/useMediaQuery";
import chzzkLogo from './chzzklogo_kor(Green).svg';

const BiasPage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');


    if (isMobile){
        return(
            <BiasPageMobile/>
        );
    }else{
        return(
            <DesktopLayout>
                <BiasPageDesktop/>
            </DesktopLayout>
        );
    }
}


const BiasPageMobile = () => {
    const schedules = [
        { date: "25년 09월 29일", sid:"1", weekday: "월요일", title: "콘텐츠 제목 1", startTime: "오후 01시 시작", tags: ["태그1"] },
        { date: "25년 09월 30일", sid:"2", weekday: "화요일", title: "콘텐츠 제목 2", startTime: "오후 03시 시작", tags: ["태그2"] },
        { date: "25년 10월 01일", sid:"3", weekday: "수요일", title: "콘텐츠 제목 3", startTime: "오전 11시 시작", tags: ["태그3"] },
        { date: "25년 10월 02일", sid:"2", weekday: "목요일", title: "콘텐츠 제목 2", startTime: "오후 03시 시작", tags: ["태그2"] },
        { date: "25년 10월 03일", sid:"", weekday: "금요일", title: "콘텐츠 제목 3", startTime: "오전 11시 시작", tags: ["태그3"] },
        { date: "25년 10월 04일", sid:"4", weekday: "토요일", title: "콘텐츠 제목 2", startTime: "오후 03시 시작", tags: ["태그2"] },
        { date: "25년 10월 05일", sid:"5", weekday: "일요일", title: "콘텐츠 제목 3", startTime: "오전 11시 시작", tags: ["태그3"] },
    ];

    // 7개 고정
    const weekSchedules = Array.from({ length: 7 }, (_, idx) => schedules[idx] || {
        date: "", weekday: "", title: "", startTime: "", tags: []
    });

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
                            <div className={style["bias-state"]}>임시 등록</div>
                            <div className={style["bias-name"]}>도롱햄</div>
                        </div>
                        <div className={style["bias-platform-container"]}>
                            <div className={style["platform-image"]}>
                                <img src={chzzkLogo}/>
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
                    <div className={style["week-data"]}>9월 5주차 콘텐츠</div>
                    <div className={style["week-select-button-wrapper"]}>
                        <div className={style["prev-button"]}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" fill="white"/>
                                <path d="M14 5L7.06667 10.2C6.53333 10.6 6.53333 11.4 7.06667 11.8L14 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>
                        <div className={style["next-button"]}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                <rect width="22" height="22" rx="11" transform="matrix(-1 0 0 1 22 0)" fill="white"/>
                                <path d="M8 5L14.9333 10.2C15.4667 10.6 15.4667 11.4 14.9333 11.8L8 17" stroke="#24272C" strokeWidth="1.5" strokeLinecap="round"/>
                            </svg>
                        </div>
                    </div>
                </div>
                <motion.div
                    className={style["schedule-list-wrapper"]}
                    initial="hidden"
                    animate="visible"
                    variants={containerVariants}
                >
                    {weekSchedules.map((schedule, idx) => (
                        <motion.div
                            key={idx}
                            className={style["single-schedule-wrapper"]}
                            variants={itemVariants}
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
                            {
                                schedule.sid != "" ? (
                                    <div className={style["single-schedule-container"]}>
                                        <div className={style["single-schedule-image"]}></div>
                                        <div className={style["single-schedule-detail-wrapper"]}>
                                            <div className={style["single-schedule-title"]}>
                                                {schedule.title || "콘텐츠 없음"}
                                            </div>
                                            <div className={style["single-start-time"]}>
                                                {schedule.startTime || ""}
                                            </div>
                                            <div className={style["schedule-tag-wrapper"]}>
                                                {schedule.tags.length > 0 ? (
                                                    schedule.tags.map((tag, tIdx) => (
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
                                ):(
                                    <div className={style["single-schedule-container"]}>
                                        <div className={style["single-schedule-image"]}>
                                            <img src={"https://kr.object.ncloudstorage.com/nova-images/no-image.png"}/>
                                        </div>
                                        <div className={style["empty-schedule"]}> 휴방 / 미지정</div>
                                    </div>
                                )
                            }
                        </motion.div>
                    ))}
                </motion.div>

                <div className={style["background-gradient"]}>
                    <img src={background}/>
                </div>
            </div>
        </div>
    );
};

export default BiasPage;
