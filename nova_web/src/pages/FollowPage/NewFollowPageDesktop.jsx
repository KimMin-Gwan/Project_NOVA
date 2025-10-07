import { useEffect, useState, useRef } from "react";
import style from "./NewFollowPageDesktop.module.css";
import chzzklogo from "./chzzklogo_kor(Green).svg";
import sooplogo from "./SOOP_LOGO_Blue 1.png";
import biasPlusIcon from "./plus_icon.svg";
import { useNavigate } from "react-router-dom";
import { BIAS_URL, DEFAULT_BIAS_URL } from "../../constant/biasUrl";

import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';
import { FreeMode} from 'swiper/modules';


const FollowPageDesktop = ({
    tags, targetPlatform, setTargetPlatform, biasList, searchResult, searchWord,
    handleSearchWord, handleKeyDown, fetchSearchBias
}) =>{
    const navigate = useNavigate();
    
    const onClickComponent = (bias) => {
        const scrollContainer = document.getElementById("desktop-scroll-container");
        const currentScroll = scrollContainer ? scrollContainer.scrollTop : window.scrollY;

        // ✅ 세션 저장
        sessionStorage.setItem(
            "followPageState",
            JSON.stringify({
            biasList,
            searchResult,
            searchWord,
            targetPlatform,
            scrollY: currentScroll,
            })
        );
        // ✅ 페이지 이동
        navigate(`/bias/${bias.bid}`, {
            state: { fromFollow: true },
        });
    }

    const handleFetchMore = async () => {
        const res = await fetchSearchBias(searchWord, targetPlatform, searchResult.length, true)
        if (!res){
            if (window.confirm("더 이상 표시할 스트리머가 없습니다. 스트리머 등록 페이지로 이동할까요?")) {
                    navigate("/submit_new");
                }
        }
    }

    const handleChangePlatform = async (tag) => {
        setTargetPlatform(tag);
        await fetchSearchBias(searchWord, tag, 0, false)
    }

    return(
        <div className={style["following-page-frame"]}>
            <div className={style["bias-select-container"]}>
                <span className={style["bias-select-section-title"]}>팔로우 중인 스트리머</span>
                <div className={style["bias-selection-wrapper"]} >
                    <Swiper
                        slidesPerView={"auto"}
                        spaceBetween={30}
                        modules={[FreeMode]}
                    >
                        <SwiperSlide 
                            style={{ width: "205px"}}
                        >
                            <AddNewBiasComponent/>
                        </SwiperSlide>
                        {biasList.map((bias) => (
                            <SwiperSlide
                                key={bias.bid}
                                style={{ width: "205px"}}
                            >
                                <BiasComponent
                                    bias={bias}
                                    onClickComponent={onClickComponent}
                                />
                            </SwiperSlide>
                        ))}
                    </Swiper>
                </div>
            </div>
            <div className={style["follow-search-container"]}>
                <div className={style["search_input_wrapper"]}>
                    <input className={style["search_input"]}
                        onKeyDown={handleKeyDown}
                        onChange={(e) => {
                            handleSearchWord(e);
                        }}
                        placeholder="슈퍼노바에 등록된 스트리머를 검색 할 수 있어요."
                        type="text"
                    />
                </div>
                <div className={style["follow-search-options-wrapper"]}>
                    {   
                        tags.map((tag) => {
                            return(
                                <Tag key={tag} tag={tag} targetPlatform={targetPlatform}
                                    handleChangePlatform={handleChangePlatform}
                                />
                            )
                        })
                    }
                </div>
            </div>
            <div className={style["search-result-container"]}>
                <div className={style["search-result-grid"]}>
                {   
                    searchResult.map((searchedBias, index) => {
                        return(
                            <div className={style["grid-component-wrapper"]}
                                key={index}
                            >
                                <BiasComponent 
                                    bias={searchedBias}
                                    onClickComponent={onClickComponent}
                                />
                            </div>
                        )
                    })
                }
                </div>
                <div className={style["more-button"]}
                    onClick={handleFetchMore}
                >
                    더 불러오기
                </div>
            </div>
        </div>
    );
}

const Tag = ({tag, targetPlatform, handleChangePlatform}) => {
    return(
        <div className={style["tag-wrapper"]}
            style={{
                border : targetPlatform == tag ? "2px solid #fff" : "2px solid #3FAFFF",
                background: targetPlatform == tag? "#3FAFFF" : "#fff",
                color: targetPlatform == tag? "#fff" : "#222"
            }}
            onClick={()=>{handleChangePlatform(tag)}}
        >
            {tag}
        </div>
    );
}


const BiasComponent = ({
    bias, onClickComponent
}) => {

    return(
        <div className={style["bias-component-wrapper"]}
            onClick={()=>{
                onClickComponent(bias)
            }}
        >
            <div className={style["bias-component"]}
                onClick={()=>{console.log(bias.bname)}}
            >
                <div className={style["bias-image"]}>
                    <img
                      src={BIAS_URL + `${bias.bid}.png`}
                        onError={(e) => {
                            e.currentTarget.onerror = null; // 무한 루프 방지
                            e.currentTarget.src = DEFAULT_BIAS_URL;
                        }}
                        alt="bias"
                      />
                </div>
                <div className={style["bias-detail-wrapper"]}>
                    <span className={style["bias-name"]}> {bias.bname}</span>
                    {
                        bias.platform == "치지직" ? (
                            <img className={style["bias-platform-logo"]} src={chzzklogo}/>
                        ):(
                            <img className={style["bias-platform-logo"]} src={sooplogo}/>
                        )
                    }
                </div>
            </div>
        </div>
    );
}

const AddNewBiasComponent = () => {
    const navigate = useNavigate();

    const handleAddNewBias = () => {
        navigate("/submit_new");
    }

    return(
        <div className={style["bias-component-wrapper"]}>
            <div className={style["add-bias-component"]} 
                onClick={handleAddNewBias}
            >
                <span className={style["bias-name"]}> 스트리머 등록하기</span>
                <img className={style["bias-plus-icon"]} src={biasPlusIcon}/>
            </div>
        </div>
    );
}

export default FollowPageDesktop;