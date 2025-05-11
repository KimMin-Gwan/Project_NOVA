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
                    </div>
                </SwiperSlide>
            </Swiper>
        </div>
    </div>
  );
}