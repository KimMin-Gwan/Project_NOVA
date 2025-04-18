import { useNavigate } from "react-router-dom";
import React, { useEffect, useState, useRef } from "react";
// Swiper 관련 모듈
import { FreeMode, Pagination } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";

import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

import style from "./ScheduleMakePage.module.css"; // CSS 모듈 임포트

const textContentList = [
    "새로운 일정을 등록할 목표 주제를 정해주세요!",
    "이미 등록된 일정을 미리 확인해보세요!",
    "일정의 상세 정보를 입력해주세요!",
    "입력한 일정을 검토하여 마무리하세요!"
]




const ScheduleMakePage = () => {
    const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
    const navigate = useNavigate();

    // 슬라이드 애니메이션 실행 함수
    const executeSlideAnimation = (slideId) => {
        const swiperSlide = document.getElementById(slideId);
        const slideTitleBox = swiperSlide?.querySelector("#slideTitleBox");
        const slideStepTitle = swiperSlide?.querySelector("#slideStepTitle");
        const slideStepSubtitle = swiperSlide?.querySelector("#slideStepSubtitle");
        const slideBodyContainer = swiperSlide?.querySelector("#slideBodyContainer");
        const slideBottomContainer = swiperSlide?.querySelector("#slideBottomContainer");

        if (swiperSlide && slideTitleBox && slideStepTitle && slideStepSubtitle && slideBodyContainer) {
            setTimeout(() => {
                // subtitle 숨기기
                slideStepSubtitle.style.opacity = 0;

                // titleBox와 title 크기 변경
                setTimeout(() => {
                    slideTitleBox.style.height = "250px";
                    slideStepTitle.style.fontSize = "26px";
                    slideBodyContainer.style.height = "675px";
                    slideBottomContainer.style.height = "150px"; // 하단 컨테이너 숨기기

                    // subtitle 텍스트 변경 후 나타나기
                    setTimeout(() => {
                        slideStepSubtitle.textContent = textContentList[swiperRef.current?.activeIndex];
                        slideStepSubtitle.style.opacity = 1;
                        slideStepSubtitle.style.fontSize = "17px";
                        slideBodyContainer.style.opacity = 1;
                        slideBottomContainer.style.opacity = 1; // 하단 컨테이너 나타나기
                    }, 1000); // titleBox와 title 애니메이션이 끝난 후 실행
                }, 500); // subtitle 사라지는 애니메이션 시간
            }, 1000); // 1초 후 애니메이션 시작
        }
    };

    // 슬라이드 변경 시 애니메이션 실행
    const handleSlideChange = () => {
        const currentIndex = swiperRef.current?.activeIndex;
        const slideId = `swiperSlide${currentIndex + 1}`; // 슬라이드 ID 계산

        if (currentIndex === 0) {
            // 첫 번째 슬라이드에서 두 번째 슬라이드로 이동할 때 애니메이션 실행
            executeSlideAnimation(slideId);
        }else {
            // 화면 위로 스크롤
            setTimeout(() => {
                window.scrollTo({ top: 0, behavior: "smooth" });
                executeSlideAnimation(slideId);
            }, 500); // 1초 대기 후 스크롤 이동
        }
    };

    useEffect(() => {
        const currentIndex = swiperRef.current?.activeIndex;
        const slideId = `swiperSlide${currentIndex + 1}`; // 슬라이드 ID 계산
        setTimeout(() => {
            executeSlideAnimation(slideId);
        }, 1000)
    }, [swiperRef.current?.activeIndex]);

  return (
    <div className="container">
        <div className={style["body-container"]} >
            <Swiper 
                style={{width: "100%", height: "100%"}}
                direction={'vertical'}
                onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
                onSlideChange={handleSlideChange} // 슬라이드 변경 이벤트
                speed={1000} // 슬라이드 전환 속도 1초
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
                                        <div className={style["target-bias"]}></div>
                                        <span className={style["top-box-content"]}> 
                                            선택된 주제
                                        </span>
                                    </div>
                                    <div className={style["slide-body-bottom-box"]}> 컨텐츠 </div>
                                </div>
                            </div>
                            <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                <div className={style["bottom-button"]}>
                                    취소
                                </div>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slideNext()} // 오른쪽 슬라이드 이동
                                >
                                    선택 완료
                                </div>
                            </div>
                    </div>
                </SwiperSlide>
                <SwiperSlide>
                    <div id="swiperSlide2" className={style["swiper-slide"]}>
                        <div id ="slideTitleBox" className={style["slide-title-box"]}>
                            <span id="slideStepTitle" className={style["slide-step-title"]}> 2단계 </span>
                            <span id="slideStepSubtitle" className={style["slide-step-subtitle"]}> 중복 확인</span>
                        </div>
                            <div id="slideBodyContainer" className ={style["slide-body-container"]}>
                                <div className={style["slide-box-wrapper"]}>
                                    <div className={style["slide-body-top-box"]}>
                                        <div className={style["target-bias"]}></div>
                                        <span className={style["top-box-content"]}> 
                                            선택된 주제
                                        </span>
                                    </div>
                                    <div className={style["slide-body-bottom-box"]}> 컨텐츠 </div>
                                </div>
                            </div>
                            <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                >
                                    이전
                                </div>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slideNext()} // 오른쪽 슬라이드 이동
                                >
                                    확인 완료
                                </div>
                            </div>
                    </div>
                </SwiperSlide>
                <SwiperSlide>
                    <div id="swiperSlide3" className={style["swiper-slide"]}>
                        <div id ="slideTitleBox" className={style["slide-title-box"]}>
                            <span id="slideStepTitle" className={style["slide-step-title"]}> 3단계 </span>
                            <span id="slideStepSubtitle" className={style["slide-step-subtitle"]}> 일정 작성</span>
                        </div>
                            <div id="slideBodyContainer" className ={style["slide-body-container"]}>
                                <div className={style["slide-box-wrapper"]}>
                                    <div className={style["slide-body-bottom-box"]}> 컨텐츠 </div>
                                </div>
                            </div>
                            <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                >
                                    이전으로
                                </div>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slideNext()} // 오른쪽 슬라이드 이동
                                >
                                    작성 완료
                                </div>
                            </div>
                    </div>
                </SwiperSlide>
                <SwiperSlide>
                    <div id="swiperSlide4" className={style["swiper-slide"]}>
                        <div id ="slideTitleBox" className={style["slide-title-box"]}>
                            <span id="slideStepTitle" className={style["slide-step-title"]}> 4단계 </span>
                            <span id="slideStepSubtitle" className={style["slide-step-subtitle"]}> 일정 검토</span>
                        </div>
                            <div id="slideBodyContainer" className ={style["slide-body-container"]}>
                                <div className={style["slide-box-wrapper"]}>
                                    <div className={style["slide-body-top-box"]}>
                                        <span className={style["top-box-content"]}> 
                                            총 5개의 일정을 작성했어요.
                                        </span>
                                    </div>
                                    <div className={style["slide-body-bottom-box"]}> 컨텐츠 </div>
                                </div>
                            </div>
                            <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                >
                                    이전으로
                                </div>
                                <div className={style["bottom-button"]}
                                    onClick={() => swiperRef.current?.slideNext()} // 오른쪽 슬라이드 이동
                                >
                                    등록
                                </div>
                            </div>
                    </div>
                </SwiperSlide>
                <SwiperSlide>
                    <div id="swiperSlide4" className={style["swiper-slide"]}>
                        <div id ="slideTitleBox" className={style["slide-title-box"]}>
                            <span id="slideStepTitle" className={style["slide-step-title"]}> 등록 완료 </span>
                        </div>
                    </div>
                </SwiperSlide>
            </Swiper>
        </div>
    </div>
  );
};

export default ScheduleMakePage;