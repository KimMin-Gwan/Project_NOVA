import style from "./BiasPageDesktop.module.css";

import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';
import { FreeMode} from 'swiper/modules';
import chzzkLogo from './chzzklogo_kor(Green).svg';

const BiasPageDesktop = () => {

    const schedules = [
        { date: "25년 09월 29일", sid:"1", weekday: "월요일", title: "콘텐츠 제목 1", startTime: "오후 01시 시작", tags: ["태그1"] },
        { date: "25년 09월 30일", sid:"2", weekday: "화요일", title: "콘텐츠 제목 2", startTime: "오후 03시 시작", tags: ["태그2"] },
        { date: "25년 10월 01일", sid:"3", weekday: "수요일", title: "콘텐츠 제목 3", startTime: "오전 11시 시작", tags: ["태그3"] },
        { date: "25년 10월 02일", sid:"2", weekday: "목요일", title: "콘텐츠 제목 2", startTime: "오후 03시 시작", tags: ["태그2"] },
        { date: "25년 10월 03일", sid:"", weekday: "금요일", title: "콘텐츠 제목 3", startTime: "오전 11시 시작", tags: ["태그3"] },
        { date: "25년 10월 04일", sid:"4", weekday: "토요일", title: "콘텐츠 제목 2", startTime: "오후 03시 시작", tags: ["태그2"] },
        { date: "25년 10월 05일", sid:"5", weekday: "일요일", title: "콘텐츠 제목 3", startTime: "오전 11시 시작", tags: ["태그3"] },
    ];

    return(
        <div className={style["frame"]}>
            <div className={style["upper-section"]}>
                <div className={style["top-button-wrapper"]}>
                    <div className={style["try-search-button"]}>
                        유튜브에서 검색
                    </div>
                    <div className={style["try-follow-button"]}>
                        팔로우
                    </div>
                </div>
                <div className={style["bias-info-wrapper"]}>
                    <div className={style["bias-image-container"]}>
                        <img src={"https://kr.object.ncloudstorage.com/nova-images/ham.png"}/>
                    </div>
                    <div className={style["bias-detail-wrapper"]}>
                        <div className={style["bias-detail-container"]}>
                            <div className={style["bias-name-wrapper"]}>
                                <div className={style["bias-detail-title"]}>
                                    이름
                                </div>
                                <div className={style["bias-name"]}>
                                    도롱햄
                                </div>
                            </div>
                            <div className={style["bias-state"]}>
                                임시 등록 상태
                            </div>
                        </div>
                        <div className={style["bias-platform-container"]}>
                            <img src={chzzkLogo}/>
                        </div>
                    </div>
                </div>
            </div>

            <div className={style["schedule-section"]}>
                <div className={style["schedule-right-section"]}>
                    <div className={style["single-schedule-image"]}>
                        <img src={"https://kr.object.ncloudstorage.com/nova-images/no-image.png"}/>
                    </div>
                    <div className={style["single-schedule-detail-wrapper"]}>
                        <div className={style["single-schedule-detail-sub-wrapper"]}>
                            <div className={style["single-schedule-data-wrapper"]}>
                                <div className={style["single-schedule-data-title"]}>
                                    제목
                                </div>
                                <div className={style["single-schedule-data-body"]}>
                                    본문
                                </div>
                            </div>
                            <div className={style["single-schedule-data-wrapper"]}>
                                <div className={style["single-schedule-data-title"]}>
                                    제목
                                </div>
                                <div className={style["single-schedule-data-body"]}>
                                    본문
                                </div>
                            </div>
                        </div>
                        <div className={style["single-schedule-detail-sub-wrapper"]}>
                            <div className={style["single-schedule-data-wrapper"]}>
                                <div className={style["single-schedule-data-title"]}>
                                    제목
                                </div>
                                <div className={style["single-schedule-data-body"]}>
                                    본문
                                </div>
                            </div>
                            <div className={style["single-schedule-data-wrapper"]}>
                                <div className={style["single-schedule-data-title"]}>
                                    제목
                                </div>
                                <div className={style["single-schedule-data-body"]}>
                                    본문
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className={style["schedule-left-section"]}>
                    <div className={style["week-data-container"]}>
                        <div className={style["week-data"]}>
                            10월 1주차 콘텐츠
                        </div>
                        <div className={style["week-button-wrapper"]}>
                            <div className={style["week-button"]}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                    <rect x="0.5" y="0.5" width="21" height="21" rx="10.5" fill="white"/>
                                    <rect x="0.5" y="0.5" width="21" height="21" rx="10.5" stroke="#DBDBDB"/>
                                    <path d="M14 5L7.06667 10.2C6.53333 10.6 6.53333 11.4 7.06667 11.8L14 17" stroke="#24272C" stroke-width="1.5" stroke-linecap="round"/>
                                </svg>
                            </div>
                            <div className={style["week-button"]}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22" fill="none">
                                    <rect x="-0.5" y="0.5" width="21" height="21" rx="10.5" transform="matrix(-1 0 0 1 21 0)" fill="white"/>
                                    <rect x="-0.5" y="0.5" width="21" height="21" rx="10.5" transform="matrix(-1 0 0 1 21 0)" stroke="#DBDBDB"/>
                                    <path d="M8 5L14.9333 10.2C15.4667 10.6 15.4667 11.4 14.9333 11.8L8 17" stroke="#24272C" stroke-width="1.5" stroke-linecap="round"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div className={style["schedule-list-wrapper"]}>
                        <Swiper
                            slidesPerView={"auto"}
                            spaceBetween={30}
                            modules={[FreeMode]}
                            direction={"vertical"}
                        >
                            {schedules.map((schedule, index) => (
                                <SwiperSlide
                                    key={index}
                                    style={{ width: "380px", height: "fit-content"}}
                                >
                                    <ScheduleComponent
                                    />
                                </SwiperSlide>
                            ))}
                        </Swiper>
                    </div>
                </div>
            </div>
        </div>
    );
}


const ScheduleComponent = () => {
    return(
        <div className={style["schedule-component"]}>
            <div className={style["schedule-date-wrapper"]}>
                <div className={style["schedule-date"]}>
                    10월 01일
                </div>
                <div className={style["schedule-weekday"]}>
                    수요일
                </div>
            </div>
            <div className={style["schedule-detaile-wrapper"]}>
                <div className={style["schedule-title"]}>
                    콘텐츠 이름
                </div>
                <div className={style["schedule-start"]}>
                    PM 09:00 시작
                </div>
            </div>
            <div className={style["tag-wrapper"]}>
                <div className={style["tag"]}>
                    태그
                </div>
                <div className={style["tag"]}>
                    태그
                </div>
            </div>
        </div>
    );
}


export default BiasPageDesktop;
