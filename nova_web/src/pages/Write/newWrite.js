import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Swiper, SwiperSlide } from "swiper/react";

import style from './../SchedulePage/ScheduleMakePage.module.css';

export const NewFeedWritePage= () => {


  return (
    <div className='container'>
        <div className={style["body-container"]}>
            <Swiper
                style={{ width: "100%", height: "100%"}}
                direction={"vertical"}
                allowTouchMove={false}
                speed={1000}
            >
                <SwiperSlide>
                    <div id="swiperSlide1" className={style["swiper-slide"]}>
                        <div id ="slideTitleBox" className={style["slide-title-box"]}>
                            <span id="slideStepTitle" className={style["slide-step-title"]}> 1단계 </span>
                            <span id="slideStepSubtitle" className={style["slide-step-subtitle"]}> 주제 선택</span>
                        </div>
                            <div id="slideBodyContainer" className ={style["slide-body-container"]}>
                                <div className={style["slide-box-wrapper"]}>
                                    <div className={style["slide-body-top-box"]}>
                                    </div>
                                    <div className={style["slide-body-bottom-box"]}>
                                    </div>
                                </div>
                            </div>
                            <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                <div className={style["bottom-button"]}>
                                    취소
                                </div>
                                <div className={style["bottom-button"]}
                                    onClick={() => {
                               
                                }}
                                >
                                    선택 완료
                                </div>
                            </div>
                    </div>
                </SwiperSlide>
            </Swiper>
        </div>
    </div>
  );
}