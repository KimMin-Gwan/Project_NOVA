import { useEffect, useState, useRef } from "react";
import style from "./NewFollowPageMobile.module.css";
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
import Header from "../../component/Header/Header";
import useIntersectionObserver from "../../hooks/useIntersectionObserver";


const FollowPageMobile= ({
    tags, targetPlatform, setTargetPlatform, biasList, searchResult, searchWord,
    handleSearchWord, handleKeyDown, fetchSearchBias, initialLoaded
}) =>{
    const navigate = useNavigate();
    const [isLeft, setIsLeft] = useState(true);
    
    const onClickComponent = (bias) => {
        const currentScroll = window.scrollY;

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
        if (initialLoaded){
            const res = await fetchSearchBias(searchWord, targetPlatform, searchResult.length, true)
            if (!res) setIsLeft(false);
        }
    }

    const handleChangePlatform = async (tag) => {
        setTargetPlatform(tag);
        setIsLeft(true);
        await fetchSearchBias(searchWord, tag, 0, false)
    }

    const scrollRef = useRef(null);
    const targetRef = useIntersectionObserver(handleFetchMore,
        { root:scrollRef.current, threshold: 0.5 }, isLeft);

    return(
        <div className={style["following-page-frame"]}>
            <div className={style["top-bar"]}>
                <Header/>
            </div>
            <div className={style["inner-box"]}>
                <div className={style["bias-select-section"]}>
                    <span className={style["bias-select-section-title"]}>스트리머 선택</span>
                    <div className={style["bias-selection-wrapper"]} >
                        <Swiper
                            slidesPerView={"auto"}
                            spaceBetween={5}
                            modules={[FreeMode]}
                        >
                            <SwiperSlide 
                                style={{ width: "180px"}}
                            >
                                <AddNewBiasComponent/>
                            </SwiperSlide>
                            {biasList.map((bias) => (
                                <SwiperSlide
                                    key={bias.bid}
                                    style={{ width: "180px"}}
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
                <div className={style["follow-search-container-wrapper"]}>
                    <div className={style["follow-search-container"]}>
                        <span className={style["bias-select-section-title"]}>주제 탐색</span>
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
                        {   
                            searchResult.map((searchedBias) => {
                                return(
                                    <WideBiasComponent
                                        bias={searchedBias}
                                        onClickComponent={onClickComponent}
                                    />
                                )
                            })
                        }
                        {
                            !isLeft && (
                                <div className={style["more-info-wrapper"]}>
                                    <div className={style["more-info"]}>
                                        더 이상 불러올 내용이 없어요.
                                    </div>
                                    <div className={style["try-submit-new"]}
                                        onClick={()=>{
                                            navigate("/submit_new")
                                        }}
                                    >
                                        새로운 스트리머 등록하기
                                    </div>
                                </div>

                            )
                        }

                    </div>

                </div>
                <div ref={targetRef} style={{ height: "1px" }}></div>
            </div>
        </div>
    );
}

const Tag = ({tag, targetPlatform, handleChangePlatform}) => {
    return(
        <div className={style["tag-wrapper"]}
            style={{
                border : targetPlatform == tag ? "1px solid #fff" : "1px solid #D0E3FF",
                background: targetPlatform == tag? "#D0E3FF" : "#fff",
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
        <div className={style["bias-component-wrapper"]}>
            <div className={style["bias-component"]}
                onClick={()=>{
                    onClickComponent(bias)
                }}
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
                        ) : (
                            <img className={style["bias-platform-logo"]} src={sooplogo}/>
                        )
                    }
                </div>
            </div>
        </div>
    );
}

const WideBiasComponent = ({
    bias, onClickComponent,
}) => {
    const [isClicked, setIsClicked] = useState(false);

    return(
        <div className={style["wide-bias-component-wrapper"]}
            onClick={()=>{setIsClicked((prev)=>!prev)}}
        >
            <div className={style["wide-bias-component-upper-section"]}>
                <div className={style["wide-bias-image"]}>
                    <img
                      src={BIAS_URL + `${bias.bid}.png`}
                        onError={(e) => {
                            e.currentTarget.onerror = null; // 무한 루프 방지
                            e.currentTarget.src = DEFAULT_BIAS_URL;
                        }}
                        alt="bias"
                      />
                </div>
                <div className={style["wide-bias-detail-wrapper"]}>
                    <span className={style["wide-bias-name"]}> {bias.bname}</span>
                    <span className={style["wide-bias-platform"]}> {bias.platform}</span>
                </div>
            </div>
            {
                isClicked && (
                    <div className={style["wide-bias-component-button-wrapper"]}>
                        <div className={style["wide-bias-component-button1"]}
                            onClick={()=>window.open("https://supernova.io.kr", "_blank", "noopener,noreferrer")}
                        >
                            방송국 바로가기
                        </div>
                        <div className={style["wide-bias-component-button2"]}
                            onClick={()=>onClickComponent(bias)}
                        >
                            자세히보기
                        </div>
                    </div>
                )
            }
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

export default FollowPageMobile;