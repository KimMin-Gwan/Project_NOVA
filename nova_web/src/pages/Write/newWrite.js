import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Swiper } from 'swiper/types';



const NewFeedWritePage= () => {
    return (
        <div className='container'>
            <div className={style["body-container"]}>
                <Swiper
                    style={{ width: "100%", height: "100%"}}
                    direction={"vertical"}
                    allowTouchMove={false}
                    speed={1000}
                >
                    <SwpierSlide>
                    


                    </SwpierSlide>

                </Swiper>
            </div>
        </div>
    );
}