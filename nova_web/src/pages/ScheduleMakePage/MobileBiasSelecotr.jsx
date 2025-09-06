import { useEffect, useState, useRef } from "react";
import style from "./ScheduleMakePageMobile.module.css";
import chzzklogo from "./chzzklogo_kor(Green).svg";

import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';
import { FreeMode} from 'swiper/modules';

const MobileBiasSelectSection = ({ biasList,
     selectedBias, handleSelectBias 
    }) => {


    return (
        <div className={style["bias-select-section"]}>
            <span className={style["bias-select-section-title"]}>스트리머 선택</span>
            <div className={style["bias-selection-wrapper"]} >
                <Swiper
                    slidesPerView={1.3}
                    spaceBetween={10}
                    modules={[FreeMode]}
                >
                    {biasList.map((bias) => (
                        <SwiperSlide
                            key={bias.bid}
                        >
                            <BiasComponent
                                bias={bias}
                                selectedBias={selectedBias}
                                handleSelectBias={handleSelectBias}
                            />
                        </SwiperSlide>
                    ))}
                </Swiper>
            </div>
        </div>
    );
};

const BiasComponent = ({
    bias,
    selectedBias, handleSelectBias
}) => {

    return(
        <div className={style["bias-component-wrapper"]}>
            <div className={style["bias-component"]}
                onClick={()=>handleSelectBias(bias.bid)}
                style={{ border: selectedBias == bias.bid ? "2px solid #8CFF99" : "2px solid #fff" }}
            >
                <div className={style["bias-image"]}></div>
                <div className={style["bias-detail-wrapper"]}>
                    <span className={style["bias-name"]}> {bias.bname}</span>
                    <img className={style["bias-platform-logo"]} src={chzzklogo}/>
                </div>
            </div>
            {
                selectedBias == bias.bid &&
                 <span className={style["bias-selected-span"]}> 선택 </span> 
            }
        </div>
    );
}

export default MobileBiasSelectSection