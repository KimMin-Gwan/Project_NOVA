import { useEffect, useState, useRef } from "react";
import style from "./ScheduleMakePage.module.css";
import chzzklogo from "./chzzklogo_kor(Green).svg";
import biasPlusIcon from "./plus_icon.svg";
import { useNavigate } from "react-router-dom";

import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';
import { FreeMode} from 'swiper/modules';

const DesktopBiasSelectSection = ({ biasList,
     selectedBias, handleSelectBias 
    }) => {

    return (
        <div className={style["bias-select-section"]}>
            <span className={style["bias-select-section-title"]}>스트리머 선택</span>
            <div className={style["bias-selection-wrapper"]} >
                <Swiper
                    slidesPerView={"auto"}
                    spaceBetween={30}
                    modules={[FreeMode]}
                >
                    {biasList.map((bias) => (
                        <SwiperSlide
                            key={bias.bid}
                            style={{ width: "250px"}}
                        >
                            <BiasComponent
                                bias={bias}
                                selectedBias={selectedBias}
                                handleSelectBias={handleSelectBias}
                            />
                        </SwiperSlide>
                    ))}
                    <SwiperSlide 
                        style={{ width: "250px"}}
                    >
                        <AddNewBiasComponent/>
                    </SwiperSlide>
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

const AddNewBiasComponent = () => {
    const navigate = useNavigate();

    const handleAddNewBias = () => {
        navigate("/follow_page");
    }

    return(
        <div className={style["bias-component-wrapper"]}>
            <div className={style["add-bias-component"]} 
                onClick={handleAddNewBias}
            >
                    <span className={style["bias-name"]}> 팔로우 바로가기</span>
                    <img className={style["bias-plus-icon"]} src={biasPlusIcon}/>
            </div>
        </div>
    );
}


export default DesktopBiasSelectSection