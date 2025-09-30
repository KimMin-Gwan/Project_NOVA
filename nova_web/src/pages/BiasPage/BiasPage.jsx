import style from "./BiasPage.module.css";

const BiasPage = () => {

    return (
        <div className={style["frame"]}>
            <div className={style["inner-box"]}>
                <div className={style["bias-meta-data-wrapper"]}>
                    <div className={style["bias-image-wrapper"]}>
                    </div>
                    <div className={style["bias-detail-container-wrapper"]}>
                        <div className={style["bias-name-container"]}>
                            <div className={style["bias-state"]}>
                                임시 등록
                            </div>
                            <div className={style["bias-name"]}>
                                도롱햄
                            </div>
                        </div>
                        <div className={style["bias-platform-container"]}>
                            <div className={style["platform-image"]}>
                            </div>
                            <div className={style["platform-direct-link"]}>
                                바로가기
                            </div>
                        </div>
                        <div className={style["bias-meta-data-button-container"]}>
                            <div className={style["bias-meta-data-left-button"]}>
                                외부 검색
                            </div>
                            <div className={style["bias-meta-data-right-button"]}>
                                팔로우
                            </div>
                        </div>
                    </div>
                </div>

                <div className={style["body-wrapper"]}>
                    <div className={style["week-select-box"]}>
                        <div className={style["prev-button"]}>
                            이전주
                        </div>
                        <div className={style["week-data"]}>
                            9월 5주차 콘텐츠
                        </div>
                        <div className={style["next-button"]}>
                            다음주
                        </div>
                    </div>

                    <div className={style["schedule-list-wrapper"]}>

                        <div className={style["single-schedule-wrapper"]}>
                            <div className={style["schedule-datetime-wrapper"]}>
                                <div className={style["schedule-datetime"]}>
                                    25년 09월 29일
                                </div>
                                <div className={style["datetime-weekday"]}>
                                    월요일
                                </div>
                            </div>

                            <div className={style["single-schedule-container"]}>
                                <div className={style["single-schedule-image"]}>
                                </div>
                                <div className={style["single-schedule-detail-wrapper"]}>
                                    <div className={style["single-schedule-title"]}>
                                        콘텐츠 제목
                                    </div>
                                    <div className={style["single-start-time"]}>
                                        오후 01시 시작
                                    </div>
                                    <div className={style["schedule-tag-wrapper"]}>
                                        <div className={style["tag"]}>
                                            태그
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className={style["single-schedule-wrapper"]}>
                            <div className={style["schedule-datetime-wrapper"]}>
                                <div className={style["schedule-datetime"]}>
                                    25년 09월 29일
                                </div>
                                <div className={style["datetime-weekday"]}>
                                    월요일
                                </div>
                            </div>

                            <div className={style["single-schedule-container"]}>
                                <div className={style["single-schedule-image"]}>
                                </div>
                                <div className={style["single-schedule-detail-wrapper"]}>
                                    <div className={style["single-schedule-title"]}>
                                        콘텐츠 제목
                                    </div>
                                    <div className={style["single-start-time"]}>
                                        오후 01시 시작
                                    </div>
                                    <div className={style["schedule-tag-wrapper"]}>
                                        <div className={style["tag"]}>
                                            태그
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    );
}

export default BiasPage;