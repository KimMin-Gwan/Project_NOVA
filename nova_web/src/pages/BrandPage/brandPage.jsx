import { useState, useRef, useEffect } from "react";
import style from "./brandPage.module.css";

import brandBackgroundImage from "./brand-background.svg";
import buttonStar from "./Star_fill.svg";
import chzzkLogo from "./chzzklogo_kor(Green) 1.png";
import soopLogo from "./SOOP_LOGO_Blue 1.png";
import youtubLogo from "./youtube logo 04 1.png";
import footerImage from "./footer-image.png";
import intro1 from "./intro1.png";
import intro2 from "./intro2.png";
import intro3 from "./intro3.png";
import intro4 from "./intro4.png";
import external from "./External.svg";

import icon1 from "./icon1.png";
import sample1 from "./sample1.png";
import sample2 from "./sample2.png";
import sample3 from "./sample3.png";

import Card from "./carosel/Card.jsx";
import Carousel from "./carosel/Carosel.jsx"

import { config } from "react-spring";
import { useDrag } from "@use-gesture/react";

import { useNavigate } from "react-router-dom";



export default function BrandPage() {
    const targetRef1 = useRef(null);
    const targetRef2 = useRef(null);
    const targetRef3 = useRef(null);

    const scrollToSection1 = () => {
        targetRef1.current?.scrollIntoView({ behavior: "smooth" });
    };

    const scrollToSection2 = () => {
        targetRef2.current?.scrollIntoView({ behavior: "smooth" });
    };

    const scrollToSection3 = () => {
        targetRef3.current?.scrollIntoView({ behavior: "smooth" });
    };
    //const { brandId } = useParams();
    //const [brandData, setBrandData] = useState(null);
    //const [loading, setLoading] = useState(true);
    //const brandRef = useRef(null);

    console.log(targetRef1)

    const temp = " © 2025 TEAM SUPERNOVA. All rights reserved."
    const temp2 =" 대표 : 김민관 | 이메일: youth0828@naver.com"
    return (
        <div className={style["brand-page-background"]} >
            <TopBar
             scrollToSection1={scrollToSection1}
             scrollToSection2={scrollToSection2}
             scrollToSection3={scrollToSection3}
             />
            <BrandHighlight />
            <div className={style["brand-page-content"]}>
                <AppServices1 targetRef={targetRef1}/>
                <AppServices2 targetRef={targetRef2} />
                <AppServices3 targetRef={targetRef3} />
                <BottomFooter/>
            </div>

            <div className={style["brand-page-footer"]}>
                <span>
                    {temp}
                </span>
                <span>
                    {temp2}
                </span>
            </div>
        </div>

        
    );
}


function TopBar({scrollToSection1, scrollToSection2, scrollToSection3}) {

  const navigate = useNavigate();

  // 네비게이션 함수
  const handleNavigate = (path) => {
    navigate(`${path}`);
  };

    return (
        <div className={style["topBar-frame"]}>
            <div className={style["topBar-div"]}>
                <div className={style["topBar-text-wrapper"]}
                    onClick={()=>scrollToSection1()}
                >
                    앱 소개
                </div>
                <div className={style["topBar-text-wrapper"]}
                    onClick={()=>scrollToSection2()}
                >
                    전용 컨텐츠
                </div>
                <div className={style["topBar-text-wrapper"]}
                    onClick={()=>scrollToSection3()}
                >
                    운영자 정보
                </div>
            </div>
            <div className={style["topBar-div-2"]}>
                <div className={style["topBar-button-1"]}
                    onClick={() => handleNavigate("/signup")}>
                    회원가입
                </div>
                <div className={style["topBar-button-2"]}
                    onClick={() => handleNavigate("/novalogin")}>
                로그인
                </div>
            </div>
        </div>
    );
}

function BrandHighlight() {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(`${path}`);
  };

  const openNewWindow = () => {
    window.open(
      "https://supernova.io.kr", // 새 창에 열 URL
      "_blank", // 새로운 탭 또는 창으로 열기
      "width=600,height=900" // 창의 크기 및 기타 옵션
    );
  };
  const url = "https://supernova.io.kr/content";

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
                        <div className={style["button-1"]}
                            onClick={() => handleNavigate("/signup")}>
                            회원가입
                        </div>
                        <div className={style["button-2"]}
                            onClick={() => openNewWindow()}>
                            바로가기
                        </div>
                    </div>
                </div>
                <div className={style["brand-highlight-button-wrapper"]}>
                    <span> 컨텐츠를 즐기러 온 스트리머는! </span>
                    <div className={style["brand-highlight-button"]}
                        onClick={() => window.open(url, "_blank")}
                    >
                        <img src={buttonStar} alt="button image" className={style["brand-highlight-button-image"]} />
                        <span>
                                컨텐츠 클럽 바로가기
                        </span>
                    </div>
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
            <img src={image} className={style["big-image-container"]}/>

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
                <img className={style["middle-image-container"]}
                    src={image}
                />
            </div>
        </div>
    )
}


function AppServices1({targetRef}){

    const title = "SUPERNOVA.io.kr 에서 제공하는 기능들";
    const subtitle = "스트리머를 위한 여러가지 기능과 스트리머를 좋아하는 팬들의 팬활동을 지원하는 핵심 4가지 기능! \n 단, 사이트는 스마트폰 화면에 최적화되어 있습니다.";

    const features = [
        {
            tag1: "커뮤니티",
            tag2: "소통",
            title: "스트리머와 팬이 소통하는 커뮤니티",
            detail: "스트리머를 주제로 하는 커뮤니티에서 팬들과 소통해보세요!",
            image: intro1,
            button: "커뮤니티 바로가기"
        },
        {
            tag1: "스트리밍",
            tag2: "일정",
            title: "방송 일정과 알림 기능",
            detail: "스트리머의 방송 일정을 확인하고 다양한 컨텐츠를 탐색해보세요!",
            image: intro2,
            button: "일정 확인하기"
        },
        {
            tag1: "후기",
            tag2: "실시간",
            title: "팬들과 대중의 피드백 공간",
            detail: "컨텐츠에 대한 다양한 생각을 실시간으로 공유해요!",
            image: intro3,
            button: "컨텐츠 공유하기"
        },
        {
            tag1: "탐색",
            tag2: "컨텐츠",
            title: "등록된 컨텐츠를 탐색하고 추가하기",
            detail: "누구나 최애의 컨텐츠를 등록하거나 탐색할 수 있어요!",
            image: intro4,
            button: "컨텐츠 공유하기"
        },
    ]


    return(
        <div className={style["app-services"]} ref={targetRef}>
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

function AppServices2({targetRef}) {
    const title = "SUPERNOVA에서만 제공하는 스트리밍 전용 컨텐츠";
    const subtitle = "지원되는 플랫폼에서 스트리밍 하는 스트리머들은 누구나 사용가능!\n  SUPERNOVA의 스트리밍 전용 컨텐츠를 시청자와 함께 지금 바로 즐겨보세요!"

    let cards = [
        {
        key: "1",
        content: (
            <Card imagen={sample1}
                title={"스트리머 vs 모두의 두뇌! 실시간 [ 스무고개 ]"}
                body={"스트리머가 떠올린 정답, 시청자 여러분의 질문으로 풀어보세요. \n채팅 하나면 누구나 참여 가능! \n 하나의 질문, 수많은 추리. 집단 지성의 힘으로 정답에 다가가 보세요!"}
            />
        )
        },
        {
        key: "2",
        content: (
            <Card imagen={sample3}
                title={"시청자와 함께 하는 [ 틀린 그림 찾기 ]"}
                body={"함께 보면 더 잘 보여요!\n 여러 사람의 관찰력이 모여 정답을 찾아가는 집단 지성 기반의 실시간 협력형 콘텐츠입니다."}
            />
        )
        },
        {
        key: "3",
        content: (
            <Card imagen={sample2}
                title={"채팅으로 참여하는 노래 맞추기! [ 뮤직게서 ]"}
                body={"이 노래, 어디서 많이 들어봤는데…? \n 시청자는 채팅으로 참여해 곡명을 추리하고 정답을 맞힙니다. \n 다같이 추리하면 전부다 맞출 수 있을지도??"}
            />
        )
        }
    ];


    return(
        <div className={style["app-services"]} ref={targetRef}>
            <ServiceTitle title={title} subtitle={subtitle} />
            <div className={style["carousel-wrapper"]}>
                <Carousel
                    cards={cards}
                    height="500px"
                    width="80%"
                    margin="0 auto"
                    offset={2}
                    showArrows={false}
                />
            </div>
        </div>
    );
}

function AppServices3({targetRef}) {
    const title = "이 모든걸 만들고 운영하는 팀 [ SUPERNOVA ]는 누구?";
    const subtitle = "팀 슈퍼노바는 총 4명의 청년 개발자로 이루어진 팀입니다.\n 20대의 청춘을 바쳐 더 쉬운 스트리머 활동과 더 포괄적인 팬활동을 위해 노력합니다. ";

    const features = [
        {
            index: "01",
            title: "쓰는 사람이 만드는 사람",
            detail: "팀 슈퍼노바는 내가 실제로 사용하는 상황을 먼저 생각합니다. \n 내 최애가 이 서비스를 사용한다면 어떤 기능이 필요할까?\n 이런 질문을 스스로에게 던지며 서비스를 만듭니다.",
            image: icon1
        },
        {
            index: "02",
            title: "오타쿠의 사명을 가진 사람",
            detail: "팀 슈퍼노바는 특정 분야를 집요하게 파는 오타쿠 들입니다. \n 이름이 슈퍼노바인 이유도 누구나 최애가 될 수 있고, 누구나 최애를 가질 수 있다는 생각에서 지었답니다.",
            image: icon1
        },
        {
            index: "03",
            title: "돈보다 낭만이 먼저인 사람",
            detail: "팀 슈퍼노바는 돈보다 낭만을 먼저 생각합니다. \n 돈? 명예? 그건 중요하지 않습니다. \n 오로지 좋아하는 것을 위해 노력합니다.",
            image: icon1
        }
    ];


    return(
        <div className={style["app-services"]} ref={targetRef}>
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
    const url = "https://projectsupernova.notion.site"; // 우리 브랜드 Notion
    return(
        <div className={style["footer-info-box"]}>
            <div className={style["footer-info-box-wrapper"]}>
                <div className={style["footer-info-title"]}>{title}</div>
                <div className={style["footer-info-detail"]}>{detail}</div>
            </div>
            <div className={style["footer-info-icon-wrapper"]}>
                <img src={external} 
                    onClick={() => window.open(url, "_blank")}
                />
            </div>
        </div>
    );
}


function BottomFooter(){
    const title = "가장 빛나는 별, SUPERNOVA";
    const subtitle = "누구나 최애가 될 수 있고, 누구나 최애를 가질 수 있다.";

    const features = [
        {
            title: "팀 SUPERNOVA",
            detail: "SUPERNOVA에 대하여 자세히 알아보기",
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
