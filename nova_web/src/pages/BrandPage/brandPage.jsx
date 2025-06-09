import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import style from "./brandPage.module.css";

import brandBackgroundImage from "./brand-background.svg";
import buttonStar from "./Star_fill.svg";
import chzzkLogo from "./chzzklogo_kor(Green) 1.png";
import soopLogo from "./SOOP_LOGO_Blue 1.png";
import youtubLogo from "./youtube logo 04 1.png";
import footerImage from "./footer-image.png";

import Carousel from "react-spring-3d-carousel";
import { config } from "react-spring";
import { useDrag } from "@use-gesture/react";




export default function BrandPage() {
    //const { brandId } = useParams();
    //const [brandData, setBrandData] = useState(null);
    //const [loading, setLoading] = useState(true);
    //const brandRef = useRef(null);

    const temp = " © 2023 SUPERNOVA. All rights reserved."
    return (
        <div className={style["brand-page-background"]} >
            <TopBar />
            <BrandHighlight />
            <div className={style["brand-page-content"]}>
                <AppServices1/>
                <AppServices2/>
                <AppServices3/>
                <BottomFooter/>
            </div>

            <div className={style["brand-page-footer"]}>
                {temp}
            </div>
        </div>

        
    );
}


function TopBar() {
    return (
        <div className={style["topBar-frame"]}>
            <div className={style["topBar-div"]}>
                <div className={style["topBar-text-wrapper"]}>
                    앱 소개
                </div>
                <div className={style["topBar-text-wrapper"]}>
                    전용 컨텐츠
                </div>
                <div className={style["topBar-text-wrapper"]}>
                    운영자 정보
                </div>
            </div>
            <div className={style["topBar-div-2"]}>
                <div className={style["topBar-button-1"]}>회원가입</div>
                <div className={style["topBar-button-2"]}>로그인</div>
            </div>
        </div>
    );
}

function BrandHighlight() {
    return (
        <div className={style["brand-highlight"]}>
            <div className={style["brand-highlight-content"]}>
                <div className={style["brand-details"]}>
                    <div className={style["brand-main-title"]}>
                        슈퍼노바, 스트리머와 팬이 하나되는 공간
                    </div>
                    <div className={style["brand-subtitle"]}>
                        다양한 커뮤니티와 방송 일정을 한눈에 확인하고, 컨텐츠를 공유해보세요!
                    </div>
                    <div className={style["button-div"]}>
                        <div className={style["button-1"]}>회원가입</div>
                        <div className={style["button-2"]}>바로가기</div>
                    </div>
                </div>
                <div className={style["brand-highlight-button"]}>
                    <img src={buttonStar} alt="button image" className={style["brand-highlight-button-image"]} />
                    <span className={style["brand-highlight-button-text"]}>스트리머 주제 등록하기</span>
                </div>
                <div className={style["platforms-div"]}>
                    <div className={style["sites-box"]}>
                        <img src={chzzkLogo} className={style["platform-icon"]} alt="Platform Icon" />
                    </div>
                    <div className={style["sites-box"]}>
                        <img src={youtubLogo} className={style["platform-icon"]} alt="Platform Icon" />
                    </div>
                    <div className={style["sites-box"]}>
                        <img src={soopLogo} className={style["platform-icon"]} alt="Platform Icon" />
                    </div>
                </div>
            </div>

            <img src={brandBackgroundImage} alt="Brand Highlight" className={style["brand-highlight-background-image"]} />
        </div>
    );
}

function ServiceTitle({title, subtitle}){

    return(
        <div className={style["service-title-wrapper"]}>
            <div className={style["service-title"]}>{title}</div>
            <div className={style["service-sub-title"]}>{subtitle}</div>
        </div>
    )
}

function BigContentContainer({tag1, tag2, title, detail, image, button}){
    return (
        <div className={style["big-content-container"]}>
            <div className={style["big-image-container"]}>
                이미지
            </div>

            <div className={style["big-content-tag-container"]}>
                <div className={style["big-content-tag1"]}>{tag1}</div>
                <div className={style["big-content-tag2"]}>{tag2}</div>
            </div>
            <div className={style["big-content-title"]}>{title}</div>
            <div className={style["big-content-detail"]}>{detail}</div>
        </div>
    )
}

function MiddleContentContainer({index, title, detail, image}){
    return (
        <div className={style["middle-content-container"]}>
            <div className={style["middle-content-index"]}>{index}</div>
            <div className={style["middle-content-wrapper"]}>
                <div className={style["middle-content-title"]}>{title}</div>
                <div className={style["middle-content-detail"]}>{detail}</div>
            </div>

            <div className={style["middle-image-wrapper"]}>
                <div className={style["middle-image-container"]}>
                    아이콘
                </div>
            </div>
        </div>
    )
}

const MyCarousel = () => {
    const slides = [
        { key: 1, content:
            <div className={style["slider-container"]}>Slide 1</div> 
        },
        { key: 2, content:
            <div className={style["slider-container"]}>Slide 2</div> 
        },
        { key: 3, content:
            <div className={style["slider-container"]}>Slide 3</div> 
        },
    ];

    const [goToSlide, setGoToSlide] = useState(0);

    const bind = useDrag(({ swipe: [swipeX], velocity, direction: [xDir] }) => {
        if (Math.abs(swipeX) > 0 || velocity > 0.2) {
            const nextSlide = xDir > 0 ? goToSlide - 1 : goToSlide + 1;
            setGoToSlide((nextSlide + slides.length) % slides.length);
        }
    });

    return (
        <div {...bind()} style={{ width: "80%", height: "300px", margin: "0 auto", touchAction: "pan-y" }}>
            <Carousel
                slides={slides}
                goToSlide={goToSlide}
                offsetRadius={2}
                animationConfig={config.gentle}
            />
        </div>
    );
};

function AppServices1(){
    const title = "SUPERNOVA.io.kr 에서 제공하는 기능들";
    const subtitle = "스트리머를 위한 여러가지 기능과 스트리머를 좋아하는 팬들의 팬활동을 지원하는 핵심 4가지 기능!"

    const features = [
        {
            tag1: "커뮤니티",
            tag2: "소통",
            title: "스트리머와 팬이 소통하는 커뮤니티",
            detail: "스트리머를 주제로 하는 커뮤니티에서 팬들과 소통해보세요!",
            image: "https://example.com/community-image.png",
            button: "커뮤니티 바로가기"
        },
        {
            tag1: "컨텐츠",
            tag2: "탐색",
            title: "방송 일정과 알림 기능",
            detail: "스트리머의 방송 일정을 확인하고 다양한 컨텐츠를 탐색해보세요!",
            image: "https://example.com/schedule-image.png",
            button: "일정 확인하기"
        },
        {
            tag1: "공유",
            tag2: "팬활동",
            title: "팬들과 컨텐츠를 공유하는 공간",
            detail: "팬들이 만든 컨텐츠를 공유하고 즐길 수 있는 공간입니다.",
            image: "https://example.com/content-image.png",
            button: "컨텐츠 공유하기"
        },
        {
            tag1: "후기",
            tag2: "피드백",
            title: "팬들과 대중의 피드백 공간",
            detail: "팬들과 대중의 피드백을 받아보세요!",
            image: "https://example.com/content-image.png",
            button: "컨텐츠 공유하기"
        }
    ]


    return(
        <div className={style["app-services"]}>
            <ServiceTitle title={title} subtitle={subtitle} />
            <div className={style["service-wrapper"]}>
                {features.map((feature, index) => (
                    <BigContentContainer
                        key={index}
                        tag1={feature.tag1}
                        tag2={feature.tag2}
                        title={feature.title}
                        detail={feature.detail}
                        image={feature.image}
                        button={feature.button}
                    />
                ))}
            </div>
        </div>
    );
}

function AppServices2(){
    const title = "SUPERNOVA에서만 제공하는 스트리밍 전용 컨텐츠";
    const subtitle = "지원되는 플랫폼에서 스트리밍 하는 스트리머들은 누구나 사용가능!\n  SUPERNOVA의 스트리밍 전용 컨텐츠를 시청자와 함께 지금 바로 즐겨보세요!"

    return(
        <div className={style["app-services"]}>
            <ServiceTitle title={title} subtitle={subtitle} />
            <div className={style["carousel-wrapper"]}>
                <MyCarousel/>
            </div>
        </div>
    );
}

function AppServices3(){
    const title = "이 모든걸 만들고 운영하는 팀 [ SUPERNOVA ]는 누구?";
    const subtitle = "20대의 열정을 바쳐 더 쉬운 스트리머 활동과 더 포괄적인 팬활동을 위해 노력합니다. ";

    const features = [
        {
            index: "01",
            title: "패기와 젊음",
            detail: "슈퍼노바 팀은 젊은 열정과 패기로 새로운 아이디어를 실현합니다.",
            image: "https://example.com/team-image1.png"
        },
        {
            index: "02",
            title: "협업과 소통",
            detail: "슈퍼노바 팀은 협업과 소통을 통해 창의적인 아이디어를 공유하고 발전시킵니다.",
            image: "https://example.com/team-image2.png"
        },
        {
            index: "03",
            title: "열정과 헌신",
            detail: "슈퍼노바 팀은 열정과 헌신으로 최고의 서비스를 제공하기 위해 노력합니다.",
            image: "https://example.com/team-image3.png"
        }
    ];


    return(
        <div className={style["app-services"]}>
            <ServiceTitle title={title} subtitle={subtitle} />
            <div className={style["service-wrapper2"]}>
                {features.map((feature, index) => (
                    <MiddleContentContainer 
                        key={index}
                        index={feature.index}
                        title={feature.title}
                        detail={feature.detail}
                        image={feature.image}
                    />
                ))}
            </div>
        </div>
    );
}


function FotterInfoBox({title, detail}) {

    return(
        <div className={style["footer-info-box"]}>
            <div className={style["footer-info-box-wrapper"]}>
                <div className={style["footer-info-title"]}>{title}</div>
                <div className={style["footer-info-detail"]}>{detail}</div>
            </div>
        </div>
    );
}


function BottomFooter(){
    const title = "가장 빛나는 별, SUPERNOVA";
    const subtitle = "누구나 최애가 될 수 있고, 누구나 최애를 가질 수 있다.";

    const features = [
        {
            title: "1대1 문의",
            detail: "카카오톡 채널을 통해 1대1 문의를 할 수 있습니다."
        },
        {
            title: "이메일 문의",
            detail: "youth0828@naver.com"
        },
    ];


    return(
        <div className={style["bottom-footer-container"]}>
            <img src={footerImage} alt="Footer Background" className={style["footer-background-image"]} />
            <div className={style["footer-detail-container"]}>
                <div className={style["footer-detail-wrapper"]}>
                    <div className={style["footer-title"]}>{title}</div>
                    <div className={style["footer-subtitle"]}>{subtitle}</div>
                </div>
                <div className={style["footer-detail-wrapper2"]}>
                    {features.map((feature, index) => (
                        <FotterInfoBox 
                            key={index}
                            title={feature.title}
                            detail={feature.detail}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
