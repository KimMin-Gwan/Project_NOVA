import React, { useRef, useEffect, useState } from "react";

import style from "./ScheduleDetailDesktop.module.css";

const ScheduleDetailDekstop = () => {
    return(
        <div className={style["modal-frame"]}>
            <div className={style["modal-container"]}>
                <div className={style["modal-upper-section"]}>
                </div>
                <div className={style["modal-lower-section"]}>
                    <div className={style["schedule-tag-detail-wrapper"]}>
                        <div className={style["tag-wrapper-wrapper"]}>
                            <div className={style["tag-wrapper"]}>
                                <div className={style["tag-box"]}>
                                    태그
                                </div>
                                <div className={style["tag-box"]}>
                                    태그
                                </div>
                                <div className={style["platform-box"]}>
                                    치지직
                                </div>
                            </div>
                            <div className={style["schedule-bname"]}>
                                스트리머 이름
                            </div>
                        </div>
                        <div className={style["schedule-detail-wrapper"]}>
                            <div className={style["schedule-title"]}>
                                콘텐츠 일정 이름
                            </div>
                            <div className={style["schedule-datetime"]}>
                                <div>
                                    2025년 09월 18일 토요일
                                </div>
                                <div>
                                    |
                                </div>
                                <div>
                                    오후 06시 50분
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className={style["button-wrapper"]}>
                        <div className={style["left-button"]}>
                            플랫폼 바로가기
                        </div>
                        <div className={style["right-button"]}>
                            지금 콘텐츠 구독
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}


export default ScheduleDetailDekstop;