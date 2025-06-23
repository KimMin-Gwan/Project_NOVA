import React, { useEffect, useState, useRef } from 'react';
import brandStyle from "./../BrandPage/brandPage.module.css";
import style from "./style.module.css";


import chzzkLogo from "./../BrandPage/chzzklogo_kor(Green) 1.png";
import soopLogo from "./../BrandPage/SOOP_LOGO_Blue 1.png";
import contentBackgroundImage from "./content-background-svg.svg";

import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

export default function ContentPage (){
  const [start, setStart] = useState(false);


  const urlPath = [
    "https://naver.com",
    "https://naver.com",
  ]

  const handleNavigate = (index) => {
    window.open(urlPath(index), "_blank")
  };


  return (
    <div className={style["trick-container"]}>
    {start ? (
      <ConnectedComponent/>
    ) : (
      <IntroComponent start={start} setStart={setStart} />
    )}
    </div>
  );
}


function IntroComponent({setStart}){
  const title = "SUPERNOVA 컨텐츠 클럽에 오신걸 환영합니다.";
  const subtitle = "SUPERNOVA 컨텐츠 클럽은 방송 플랫폼에서 실시간 스트리밍을 통해 사용 가능합니다."
  return(
      <div 
        className={brandStyle["brand-page-background"]}
        style={{height: "1020px"}}
      >
        <div className={brandStyle["brand-highlight"]}
          style={{height: "1020px"}}
        >
          <div className={brandStyle["brand-highlight-content"]}
          style={{paddingTop:"336px"}}
          >
              <div className={brandStyle["brand-details"]}>
                  <div className={brandStyle["brand-main-title"]}
                  style={{width:"741px"}}
                  >
                    {title}
                  </div>
                  <div className={brandStyle["brand-subtitle"]}>
                    {subtitle}
                  </div>
              </div>
              <div className={brandStyle["platforms-div"]} >
                  <div className={brandStyle["sites-box"]}
                    onClick={()=>setStart(true)}
                  >
                      <img src={chzzkLogo} className={brandStyle["platform-icon"]} alt="Platform Icon" />
                  </div>
                  <div className={brandStyle["sites-box"]}
                    onClick={()=>setStart(false)}
                  >
                      <img src={soopLogo} className={brandStyle["platform-icon"]} alt="Platform Icon" />
                  </div>
              </div>
          </div>

          <img src={contentBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]} 
            style={{height: "1020px"}}
          />
        </div>
      </div>
  );
}

function ConnectedComponent() {
  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
  const [selectedPage, setSelectedPage] = useState(0);
  const pageTitle = "닉네임1234님 어서오세요!";
  const subTitle = "화면 오른쪽에서 ㅓ원하는 컨텐츠로 선택하세요!";


  const pages = [
    {
      index : 0,
      title: "대기실"
    },
    {
      index : 1,
      title: "스무고개"
    },
    {
      index : 2,
      title: "틀린그림찾기"
    },
    {
      index : 3,
      title: "뮤직게서"
    },
  ];

  const temp_chattings = [
    {
      _id: "1",
      body: "잠만",
    },
    {
      _id: "2",
      body: "이거 채팅임",
    },
    {
      _id: "3",
      body: "채팅 길어지는거 얼마나 길어지는지 체크해보자 이거 어떤지 보자. 얼마나 길어지니? 더 길어져야해 ㅈㅁㅈㅁ 얼마나 더 길어지냐",
    },
    {
      _id: "4",
      body: "이러면 채팅에 따라서 길어져야 하는거 아니냐",
    },
    {
      _id: "5",
      body: "채팅 예시 1",
    },
    {
      _id: "6",
      body: "채팅?",
    }
  ];



  const sliderController = (index) => {
    swiperRef.current?.slideTo(index*2);
    setSelectedPage(index);
  }

  return(
    <div>
      <Swiper
        style={{width: "100%", height: "100vh"}}
        direction={'vertical'}
        speed={1000} // 슬라이드 전환 속도 1초
        allowTouchMove={false}
        touchEventsTarget="wrapper"
        initialSlide={0}
        onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
      >
        <SwiperSlide>
          <WatiingRoomComponent
            chattings={temp_chattings}
            pages={pages}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>
        <SwiperSlide>
          <div className={style["trick-container"]}>
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <QuestionGuessorComponent
            chattings={temp_chattings}
            pages={pages}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>

        <SwiperSlide>
          <div className={style["trick-container"]}>
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <DiffGuessorComponent
            chattings={temp_chattings}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>

        <SwiperSlide>
          <div className={style["trick-container"]}>
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <MusicGuessorComponent
            chattings={temp_chattings}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>
      </Swiper>
    </div>
  );
}


function WatiingRoomComponent({chattings, pages, selectedPage, setSelectedPage}){
  const pageTitle = "닉네임1234님 어서오세요!";
  const subTitle = "화면 오른쪽에서 원하는 컨텐츠로 선택하세요!";

  const tools = [
    {
      title: "싱크 맞추기",
      subtitle : "퀴즈 맞출 땐 스트리머가 유리합니다. \n적절하게 싱크를 조절해서 공평하게 진행해요.",
      button : "싱크 맞추기"
    },
    {
      title: "방송 송출에 문제가 있나요?",
      subtitle : "문제 해결엔 재시작이 효과적이죠. \n그럼에도 여전히 문제가 있다면 알려주세요!",
      button : "나가기"
    }
  ];

  return(
    <div className={style["content-container"]}>
      <div className={style["waiting-room-side-frame"]}>
        <div className={style["sub-tools-wrapper"]}>
          <div className={style["tools-container"]}>
            <div className={style["tools-detail-wrapper"]}>
              <div className={style["tools-title"]}>
                {tools[0].title}
              </div>
              <div className={style["tools-subtitle"]}>
                {tools[0].subtitle}
              </div>
            </div>
            <button className={style["tools-button"]}
              onClick={()=>{console.log('hi')}}
            >
              {tools[0].button}
            </button>
          </div>
          <div className={style["tools-container"]}>
            <div className={style["tools-detail-wrapper"]}>
              <div className={style["tools-title"]}>
                {tools[1].title}
              </div>
              <div className={style["tools-subtitle"]}>
                {tools[1].subtitle}
              </div>
            </div>
            <button className={style["tools-button"]}
              onClick={()=>{console.log('hi')}}
            >
              {tools[1].button}
            </button>
          </div>
        </div>
      </div>
      <div className={style["waiting-room-middle-frame"]}>
        <div className={style["waiting-room-title-wrapper"]}>
          <div className={style["waiting-room-title"]}>
            {pageTitle}
          </div>
          <div className={style["waiting-room-subtitle"]}>
            {subTitle}
          </div>
        </div>
        <div className={style["chatting-preview-container"]}>
          <div className={style["chatting-title"]}>
            채팅 미리보기
          </div>
          <div className={style["chatting-wrapper"]}>
          {
            chattings.map((chatting, index) =>{
              return (
                  <Chatting key={index} index={index} body={chatting.body}/>
              );
            })
          }
          </div>
        </div>
      </div>
      <div className={style["waiting-room-side-frame"]}>
        <div className={style["pagenation-wrapper"]}>
          {
            pages.map((page, index) =>{
              return (
                <div
                  key={index}
                  className={style["pagenation-container"]}
                  style={{
                    border: selectedPage === index ? "none" : "1px solid #ccc",
                    backgroundColor: selectedPage === index ? "#fff" : "transparent",
                  }}
                  onClick={() => setSelectedPage(index)}
                >
                  {page.title}
                </div>
              );
            })
          }
        </div>
      </div>
    </div>
  );
}


function Chatting({index, body}){
  return (
    <div className={style["chatting-component"]}>
      <div className={style["chatting-box-deco"]}></div>
      <div className={style["chatting-box"]}>
        {body}
      </div>
    </div>
  );
}

const executeSlideAnimation = (id) => {
    const swiperSlide = document.getElementById(id);

    console.log(swiperSlide)
    if (swiperSlide){
        swiperSlide.style.opacity = 0;
        setTimeout(() => {
          swiperSlide.style.opacity = 1;
        }, 300); // 1초 후 애니메이션 시작
    }
};

function QuestionGuessorComponent({chattings, setSelectedPage}){
  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
  const title = "스무고개";
  const howToUse =[
    "1. 스트리머가 주제를 정합니다.",
    "2. 스트리머가 선택한 주제에 시청자가 질문합니다.",
    "3. 스트리머는 대답할 질문을 선택합니다.",
    "4. 스트리머가 질문에 '네', '아니오'로 대답합니다.",
  ];

  const [numQuestion, setNumQuestion] = useState(20);

  const option = `남은 질문 ${numQuestion}개`;
  const subOption = "클릭하여 질문 개수 조정하기";

  const [input, setInput] = useState("");
  const [target, setTarget] = useState([]);

  const handleInput = (e) => {
    const newInput = e.target.value;
    setInput(newInput); // 입력 값을 상태로 설정
  };

  const sliderController = () => {
    swiperRef.current?.slideNext();
  }

  // 슬라이드하면 나타나는 뭐시기 애니메이션인데 이거 필요없을듯
  const handlePage = (e) => {
    console.log("hello")
    const slideId = "inner-content-id"; // 슬라이드 ID 계산
    // 첫 번째 슬라이드에서 두 번째 슬라이드로 이동할 때 애니메이션 실행
    executeSlideAnimation(slideId);
  }

  return(
    <div className={style["content-container"]}
      style={{flexDirection:"column"}}
    >
      <div className={brandStyle["topBar-frame"]}>
        <div className={brandStyle["topBar-div"]}>
          <div className={brandStyle["topBar-text-wrapper"]}
            style={{width: "auto", marginTop:"20px", marginBottom: "20px"}}
            onClick={()=>setSelectedPage(0)}
          >
          대기실로 돌아가기
          </div>
        </div>
      </div>
      <div className={style["content-container-inner-wrapper"]}>
        <div className={style["content-left-container-wrapper"]}>
          <div className={style["content-info-n-how-to-use"]}>
            <span>
              {title}
            </span>
            <div className={style["how-to-use"]}>
              {
                howToUse.map((usage, index)=>{
                  return <li key={index}>{usage}</li>
                })
              }
            </div>
          </div>
          <div className={style["content-left-container"]}>
            <div className={style["chatting-preview-container"]}
              style={{padding:"16px 14px", marginTop:"0px"}}
            >
              <div className={style["chatting-wrapper"]}>
              {
                chattings.map((chatting, index) =>{
                  return (
                      <Chatting key={index} index={index} body={chatting.body}/>
                  );
                })
              }
              </div>
            </div>
          </div>
        </div>
        <Swiper
          style={{width: "100%", height: "1020px"}}
          direction={'horizontal'}
          speed={1000} // 슬라이드 전환 속도 1초
          allowTouchMove={false}
          touchEventsTarget="wrapper"
          initialSlide={0}
          onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
          onSlideChange={handlePage}
        >
          <SwiperSlide>
            <ContentIntroSlide 
              title={title}
              howToUse={howToUse}
              numQuestion={numQuestion}
              option={option}
              subOption={subOption}
              input={input}
              setInput={handleInput}
              buttonPress={sliderController}
            />
          </SwiperSlide>
          <SwiperSlide>
            <div className={style["content-container-inner-wrapper"]}>  
            </div>
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  );
}


function DiffGuessorComponent({chattings, setSelectedPage}){
  const diffSwiperRef= useRef(null);
  const title = "틀린그림찾기";
  const howToUse =[
    "1. 시청자는 좌표를 입력합니다.",
    "예시 : &12 40",
    "2. 스트리머는 클릭하여 선택합니다.",
  ];


  const option = '틀린곳 5개'

  const handleSlide = () => {
    diffSwiperRef.current?.slideNext()
  }

  return(
    <div className={style["content-container"]}
      style={{flexDirection:"column"}}
    >
      <div className={brandStyle["topBar-frame"]}>
        <div className={brandStyle["topBar-div"]}>
          <div className={brandStyle["topBar-text-wrapper"]}
            style={{width: "auto", marginTop:"20px", marginBottom: "20px"}}
            onClick={()=>{
              setSelectedPage(0);
            }}
          >
          대기실로 돌아가기
          </div>
        </div>
      </div>
      <div className={style["content-container-inner-wrapper"]}>
        <Swiper
          style={{width: "100%", height: "1020px"}}
          direction={'horizontal'}
          speed={1000} // 슬라이드 전환 속도 1초
          allowTouchMove={false}
          touchEventsTarget="wrapper"
          initialSlide={0}
        >
          <SwiperSlide>
            <ContentIntroSlide 
              chattings={chattings}
              title={title}
              howToUse={howToUse}
              option={option}
              buttonPress={handleSlide}
            />
          </SwiperSlide>
          <SwiperSlide>
            <div className={style["content-container-inner-wrapper"]}>  
            </div>
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  );
}

function MusicGuessorComponent({chattings, setSelectedPage}){
  const diffSwiperRef= useRef(null);
  const title = "뮤직게서";
  const howToUse =[
    "1. 노래 듣고 정답을 맞추는 컨텐츠입니다.",
    "2. 시청자는 채팅창에 정답을 입력합니다.",
    "3. 예시: &정답 노래이름",
    "4. 스트리머는 화면 하단에 정답을 입력합니다.",
  ];


  const option = '인트로 15초 듣기';

  const handleSlide = () => {
    diffSwiperRef.current?.slideNext()
  };

  return(
    <div className={style["content-container"]}
      style={{flexDirection:"column"}}
    >
      <div className={brandStyle["topBar-frame"]}>
        <div className={brandStyle["topBar-div"]}>
          <div className={brandStyle["topBar-text-wrapper"]}
            style={{width: "auto", marginTop:"20px", marginBottom: "20px"}}
            onClick={()=>{
              setSelectedPage(0);
            }}
          >
          대기실로 돌아가기
          </div>
        </div>
      </div>
      <div className={style["content-container-inner-wrapper"]}>
        <Swiper
          style={{width: "100%", height: "1020px"}}
          direction={'horizontal'}
          speed={1000} // 슬라이드 전환 속도 1초
          allowTouchMove={false}
          touchEventsTarget="wrapper"
          initialSlide={0}
        >
          <SwiperSlide>
            <ContentIntroSlide 
              chattings={chattings}
              title={title}
              howToUse={howToUse}
              option={option}
              buttonPress={handleSlide}
            />
          </SwiperSlide>
          <SwiperSlide>
            <div className={style["content-container-inner-wrapper"]}>  
            </div>
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  );
}

function ContentIntroSlide({
  title, howToUse, option, subOption,
  input, setInput, buttonPress
}) {

  const handleNextSlide =() => {
    if(setInput){
      if (input == ""){
        alert("정답을 입력해주세요!");
      }else{
        buttonPress()
      }
    }
  };

  console.log(setInput);

  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]} >  
      {/*여기부터 천천히 등장해야됨 */}
      <div className={style["content-body"]}>
        <div className={style["content-meta-frame"]}>
          <div className={style["content-meta-data-wrapper"]}>
            <div className={style["meta-data-clickable-div"]}> 
              <span>
                {option}
              </span>
              <li className={style["meta-data-subtitle"]}>
                {subOption}
              </li>
            </div>
          </div>
            {setInput && (
              <div className={style["content-meta-frame-input-wrapper"]}>
                <input
                  className={style["content-meta-frame-input"]}
                  value={input}
                  onChange={(e) => {
                    setInput(e);
                  }}
                  placeholder={input? input: "정답 작성"}
                  type="text"
                >
                </input>
              </div>
            )
          }
          <div className={style["content-meta-frame-input-wrapper2"]}
            onClick={()=>{handleNextSlide()}}
          >
            <span 
            >
              시작하기
            </span>
        </div>
        </div>
      </div>
    </div>
  );
}

