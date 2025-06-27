import React, { useEffect, useState, useRef } from 'react';
import { CSSTransition, TransitionGroup } from "react-transition-group";
import "./animations.css"; // CSS 애니메이션 정의
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
        style={{height: "100vh"}}
      >
        <div className={brandStyle["brand-highlight"]}
          style={{height: "100vh"}}
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
            style={{height: "100vh"}}
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
            myIndex={0}
            chattings={temp_chattings}
            pages={pages}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>
        <SwiperSlide>
          <div className={style["trick-container"]}>
            <img src={contentBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]} 
              style={{height: "100vh"}}
            />
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <QuestionGuessorComponent
            myIndex={1}
            chattings={temp_chattings}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>

        <SwiperSlide>
          <div className={style["trick-container"]}>
            <img src={contentBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]} 
              style={{height: "100vh"}}
            />
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <DiffGuessorComponent
            myIndex={2}
            chattings={temp_chattings}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
          />
        </SwiperSlide>

        <SwiperSlide>
          <div className={style["trick-container"]}>
            <img src={contentBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]} 
              style={{height: "100vh"}}
            />
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <MusicGuessorComponent
            myIndex={3}
            chattings={temp_chattings}
            selectedPage={selectedPage}
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

const executeSlideAnimation = () => {
  const className = style["content-container-inner-wrapper"];
    const swiperSlides = document.querySelectorAll(`.${className}`);

    swiperSlides.forEach((swiperSlide) => {
        swiperSlide.style.opacity = 0;
        setTimeout(() => {
          setTimeout(() => {
              swiperSlide.style.opacity = 1;
          }, 300); // 0.3초 후 애니메이션 실행
        }, 300); // 0.3초 후 애니메이션 실행
    });
};

function QuestionGuessorComponent({chattings, myIndex, selectedPage, setSelectedPage}){
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
    executeSlideAnimation();
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
      <div className={style["content-container-inner-wrapper2"]}>
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
              <QuestionGuessorPlayingSlide 
                buttonPress={sliderController}
              />
          </SwiperSlide>
          <SwiperSlide>
              <QuestionGuessorClearSlide 
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
        </Swiper>
      </div>
    </div>
  );
}


function QuestionGuessorPlayingSlide({
  buttonPress
}){
  const temp = [
    {
      body: "대충 질문 1번asgasgnqphgbeqnhlhnbalsdnhlabnlh",
      answer: 0
    },
    {
      body: "근데 ㅇㄱㅈㅉㅇㅇ 아밈누헵흄ㄴ,.휴ㅜ벰 ㅁㄶㄻ뉗ㄴㅂ미ㅏ",
      answer: 0
    },
    {
      body: "하나만 더해보자 QWER화이팅",
      answer: 0
    },
  ]

  const temp2 = [
    {
      body: "ㄹㅇ 버그투성이 개 망겜",
      answer: 1
    },
    {
      body: "ㄹㅇ 버그투성이 개 망겜",
      answer: 1
    },
    {
      body: "니가  한번 만들어봐 미친놈아",
      answer: 1
    },
    {
      body: "근데 질문 길이가 이렇게 길고 해서 좀 다루기 어ㅇ려우면 어떠헥 해야할가 더 길게 적어봐",
      answer: 3
    },
    {
      body: "니가  한번 만들어봐 미친놈아",
      answer: 2
    },
    {
      body: "근데 질문 길이가 이렇게 길고 해서 좀 다루기 어ㅇ려우면 어떠헥 해야할가 더 길게 적어봐",
      answer: 3
    },
    {
      body: "니가  한번 만들어봐 미친놈아",
      answer: 1
    },
    {
      body: "근데 질문 길이가 이렇게 길고 해서 좀 다루기 어ㅇ려우면 어떠헥 해야할가 더 길게 적어봐",
      answer: 3
    },
    {
      body: "니가  한번 만들어봐 미친놈아",
      answer: 2
    },
    {
      body: "근데 질문 길이가 이렇게 길고 해서 좀 다루기 어ㅇ려우면 어떠헥 해야할가 더 길게 적어봐",
      answer: 3
    }, 
    {
      body: "니가  한번 만들어봐 미친놈아",
      answer: 1
    },
    {
      body: "근데 질문 길이가 이렇게 길고 해서 좀 다루기 어ㅇ려우면 어떠헥 해야할가 더 길게 적어봐",
      answer: 3
    },
    {
      body: "니가  한번 만들어봐 미친놈아",
      answer: 2
    },
    {
      body: "근데 질문 길이가 이렇게 길고 해서 좀 다루기 어ㅇ려우면 어떠헥 해야할가 더 길게 적어봐",
      answer: 3
    }

  ]

  const [waitingQuestion, setWaitingQuestion] = useState(temp);
  const [answeredQuestion, setAnsweredQuestion] = useState(temp2);


  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]}
      style={{justifyContent:"center", alignItems:"flex-start", opacity:0}}
    >  
      <div className={style["content-body"]}>
        <div className={style["question-guessor-top"]}>
          <div className={style["question-guessor-top-left-box"]}>
            <div className={style["question-guessor-top-left-title-wrapper"]}>
              <span> 질문 대기</span>
              <p>최대 3개 까지 보관됩니다.</p>
            </div>
            <TransitionGroup className={style["question-guessor-top-left-body-wrapper"]}>
              {waitingQuestion.map((question, index) => (
                <CSSTransition
                  key={index}
                  timeout={300}
                  classNames="fade"
                >
                  <QuestionObject
                    question={question}
                    waitingQuestion={waitingQuestion}
                    setWaitingQuestion={setWaitingQuestion}
                    setAnsweredQuestion={setAnsweredQuestion}
                  />
                </CSSTransition>
              ))}
            </TransitionGroup>
          </div>
          <div className={style["question-guessor-top-right-wrapper"]}>
            <div className={style["stage-meta-data-box"]}>
              <span style={{color:"#111", fontSize:"36px", height:"50px"}}>
                남은 질문 20개
              </span>
              <div>
                클릭해서 질문 개수 변경
              </div>
            </div>
          </div>
        </div>
        <div className={style["question-guessor-middle-box"]}>
          <div className={style["question-guessor-middle-title-wrapper"]}>
            <span>
              답변 내역
            </span>
          </div>
          <TransitionGroup className={style["question-guessor-middle-question-wrapper"]}>
            {answeredQuestion.map((question, index) => (
              <CSSTransition
                key={index}
                timeout={300}
                classNames="fade"
              >
                <QuestionObject
                  question={question}
                  waitingQuestion={waitingQuestion}
                  setWaitingQuestion={setWaitingQuestion}
                  setAnsweredQuestion={setAnsweredQuestion}
                />
              </CSSTransition>
            ))}
          </TransitionGroup>
        </div>
        <div className={style["question-guessor-bottom"]}>
          <div className={style["question-guessor-bottom-button"]}
            onClick={()=>buttonPress()}
          >
            <span
              style={{fontSize:"36px"}}
            >
              정답 확인
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}


function QuestionGuessorClearSlide({
  buttonPress
}){
  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]} 
      style={{justifyContent:"center", alignItems:"center", opacity:0}}
    >  
      {/*여기부터 천천히 등장해야됨 */}
      <div className={style["content-meta-body"]}>
        <div className={style["content-meta-frame"]}>
          <div className={style["content-meta-frame-input-wrapper"]}
            style={{
              width: "500px",
              height: "300px",
              flexDirection: "column",
              gap: "30px"
            }}
          >
            <span
              style={{
                fontSize: "28px",
                color: "#767676"
              }}
            >
              정답
            </span>
            <span
              style={{
                fontSize: "38px",
                color: "#111"
              }}
            >
              정답은 이거랍니다.
            </span>
          </div>
          <div className={style["content-meta-frame-input-wrapper2"]}
            onClick={()=>{buttonPress()}}
          >
            <span 
            >
              다시 시작
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}


function QuestionObject({
  question, 
  waitingQuestion,
  setWaitingQuestion,
  setAnsweredQuestion
}){
  const [isClicked, setIsClicked] = useState(false);
  const [isFading, setIsFading] = useState(false);
  const s_answer = ["네", "아니오", "거절"];

  const handleClick = () => {
    setIsClicked((prev) => !prev);
  };

  const handleAnswer = (index) => {
    setIsFading(true); // 페이드 아웃 시작
    setTimeout(() => {
      // 페이드 아웃 완료 후 상태 업데이트
      const updatedWaitingQuestions = waitingQuestion.filter(
        (q) => q !== question
      );
      setWaitingQuestion(updatedWaitingQuestions);

      if (index !== 3) {
        const answered = { ...question, answer: index };
        setAnsweredQuestion((prev) => [...prev, answered]);
      }
    }, 300); // 애니메이션 지속 시간과 동일하게 설정
  };

  if(question.answer){
    return(
      <div className={style["question-object-frame"]}
        style={{maxWidth:"33%"}}
      >
        <div className={style["question-object-body"]}>
          {question.body}
        </div>
        <div className={style["question-object-interaction-wrapper"]}>
          <p>{s_answer[question.answer-1]}</p>
        </div>
      </div>
    );
  }else{
    return(
      <div
        className={`${style["question-object-frame"]} ${
          isFading ? "fade-out" : "" } question-object`}
      >
        <div className={style["question-object-body"]}
            style={{
              border : isClicked ? "2px solid #111" : "1px solid #5C5C5C"
            }}
          onClick={handleClick}
        >
          {question.body}
        </div>
        <div className={style["question-object-interaction-wrapper"]}>
          <div
            style={{
              opacity: isClicked ? "1" : "0",
              transform: isClicked ? "scale(1)" : "scale(0.9)",
              height: isClicked ? "auto" : "0",
            }}
          >
            <p onClick={() => handleAnswer(1)}
            >네
            </p><p> / </p>
            <p onClick={() => handleAnswer(2)}
            >아니오</p><p>/</p>
            <p onClick={() => handleAnswer(3)}
            >거절</p>
          </div>
        </div>
      </div>
    );
  }
}



//----------------------------------------------------------













function DiffGuessorComponent({chattings, selectedPage, myIndex, setSelectedPage}){
  const diffSwiperRef= useRef(null);
  const title = "틀린그림찾기";
  const howToUse =[
    "1. 시청자는 좌표를 입력합니다.",
    "예시 : &12 40",
    "2. 스트리머는 클릭하여 선택합니다.",
  ];

  const option = '틀린곳 5개'

  const handleSlide = () => {
    //diffSwiperRef.current?.slideNext()
    alert("아직 준비중입니다!");
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
      <div className={style["content-container-inner-wrapper2"]}>
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



//-------------------------------------------------------------------------------------------








function MusicGuessorComponent({chattings, myIndex, selectedPage, setSelectedPage}){
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
      <div className={style["content-container-inner-wrapper2"]}>
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
          onSwiper={(swiper) => (diffSwiperRef.current = swiper)} // Swiper 인스턴스 참조
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
            <MusicGuessorPlayingSlide
              buttonPress={handleSlide}
            />
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  );
}



const colorSample = ["#FFA347", "#479DFF", "#A947FF"]

function MusicGuessorPlayingSlide({buttonPress}){

  const tempMusicInfo = {
    id : 'J7klzJ9auE0',
    name : "뜨거운여름밤은가고남은것은볼품없지만"
  }

  const playerRef = useRef(null);
  const [answerFlag, setAnswerFlag] = useState(false);

  const handleShowAnswer =()=>{
    setAnswerFlag((prev)=>!prev);
  }


  useEffect(() => {
    // Load the IFrame Player API code asynchronously
    const tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // Function to create a YouTube player after the API loads
    window.onYouTubeIframeAPIReady = () => {
      playerRef.current = new window.YT.Player('player', {
        height: '80%',
        videoId: tempMusicInfo.id, // Replace with your desired video ID
        playerVars: {
          autoplay: 0, // Prevent auto-play
          controls: 1,
          playsinline: 1,
        },
      });
    };

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
      }
    };
  }, []);

  const playVideo = () => {
    if (playerRef.current) {
      playerRef.current.playVideo();
    }
  };

  const pauseVideo = () => {
    if (playerRef.current) {
      playerRef.current.pauseVideo();
    }
  };

  const stopVideo = () => {
    if (playerRef.current) {
      playerRef.current.stopVideo();
    }
  };



  const [answer, setAnswer] = useState("");

  const tempUser = [
    { id: 0, nickname: "가짜 이름 1", point: 10 },
    { id: 1, nickname: "가짜 이름 2", point: 6 },
    { id: 2, nickname: "가짜 이름 3", point: 5 },
    { id: 5, nickname: "누구겠냐~", point: 11 },
  ];

  const tempChatting = [
    { id: 4, body: "이건 뭐지", state:false},
    { id: 0, body: "정답!", state:false },
    { id: 1, body: "잠시만 저거", state:false},
    { id: 2, body: "이게정답임", state:true},
  ]

  const [sampleChatting ,setSampleChatting] = useState(tempChatting);

  const handleNewAnswer = (e) =>{
    if (e.key === 'Enter') {
      const newChatting = {
        id: sampleChatting.length,
        body: answer,
        state: false
      };
      
      if (answer === tempMusicInfo.name){
        newChatting.state = true
        setAnswerFlag(true);
      }

      setSampleChatting((prev)=>[...prev, newChatting]);
      setAnswer("");
    }
  }

  const [userList, setUserList] = useState(tempUser);
  const [top3Users, setTop3Users] = useState([]);

  useEffect(() => {
    if (userList) {
      // point 기준으로 내림차순 정렬 후 상위 3명만 선택
      const sortedTop3 = [...userList]
        .sort((a, b) => b.point - a.point)
        .slice(0, 3);
      setTop3Users(sortedTop3);
    }
  }, [userList]); // userList가 변경될 때 실행


  const handleInput = (e) => {
    const newInput = e.target.value;
    setAnswer(newInput); // 입력 값을 상태로 설정
  };

  const [counter, setCounter] = useState(15);
  const [isPlaying, setIsPlaying] = useState(false);
  const timerRef = useRef(null); // 타이머 ID를 저장할 Ref

  const handlePlaying = () => {
    const shape = document.getElementById('shape');

    if (counter === 0) {
      // 카운터가 0이면 초기화
      setCounter(15); // 초기값으로 설정
      setIsPlaying(false); // 정지 상태로 변경
      stopVideo();
    }
    if (isPlaying) {
      // 타이머가 동작 중이면 정지
      clearInterval(timerRef.current);
      timerRef.current = null;
      setIsPlaying(false);
      pauseVideo()
    } else {
      // 타이머가 멈춰있으면 시작
      timerRef.current = setInterval(() => {
        setCounter((prevCounter) => {
          if (prevCounter <= 1) {
            clearInterval(timerRef.current); // 0에 도달하면 타이머 정지
            timerRef.current = null;
            setIsPlaying(false); // 정지 상태로 전환
            stopVideo();
            return 0;
          }
          return prevCounter - 1;
        });
      }, 1000);
      setIsPlaying(true);
      playVideo();
    }
  };

  useEffect(() => {
    // 컴포넌트 언마운트 시 타이머 정리
    return () => clearInterval(timerRef.current);
  }, []);


  const ScoreComponent = ({index, nickname, point}) => {
    const color = colorSample[index]

    return(
      <div className={style["music-guessor-score-component"]}>
        <div className={style["rating-nickname-wrapper"]}>
          <p className={style["score-rating"]}
           style={{ color : color }}
          >
            {index+1}위
          </p>
          <p className={style["nickname"]}>
            {nickname}
          </p>
        </div>
        <p className={style["point"]}>
          {point}
        </p>
      </div>
    );
  }

  const AnswerChattingComponent = ({answer}) => {
    return(
      <div className={style["music-guessor-chatting-component"]}>
        <div className={style["answer-chatting"]}>
          {answer.body}
        </div>
        {
          answer.state ? (
            <p className={style["correct"]}>
              정답
            </p>
          ) : (
            <p className={style["uncorrect"]}>
              오답
            </p>
          )
        }
      </div>
    );
  }


  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]} 
      style={{justifyContent:"center", alignItems:"center", opacity:1, position:"relative"}}
    >  
      <div className={style["content-body"]}
        style={{
          position:"relative",
          zIndex: "1",
        }}
      >
        <div className={style["music-guessor-top-frame"]}>
          <div className={style["music-guessor-top-left-frame"]}>
            <div className={style["music-guessor-playing-button-wrapper"]}>
              <div className={style["music-guessor-playing-button"]}
                onClick={handlePlaying} disabled={isPlaying}
                style={{
                  position: "relative",
                  cursor: "pointer",
                  overflow: "hidden",
                }}
              >
                    {/* Pause Icon */}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="136"
                      height="136"
                      viewBox="0 0 136 136"
                      fill="none"
                      style={{
                        position: "absolute",
                        top: 85,
                        left: 84,
                        opacity: isPlaying ? 1 : 0,
                        transform: isPlaying ? "scale(1)" : "scale(0.8)",
                        transition: "opacity 0.3s ease, transform 0.3s ease",
                      }}
                    >
                      <path
                        d="M109.882 0.118578C124.242 0.118578 135.882 11.7592 135.882 26.1186V109.883C135.882 124.242 124.242 135.883 109.882 135.883H26.1178C11.7584 135.883 0.11775 124.242 0.11775 109.883V26.1186C0.11775 11.7592 11.7583 0.118578 26.1177 0.118578H109.882Z"
                        fill="url(#paint0_linear_2545_19)"
                      />
                      <defs>
                        <linearGradient
                          id="paint0_linear_2545_19"
                          x1="135.882"
                          y1="0.118578"
                          x2="32.9721"
                          y2="103.029"
                          gradientUnits="userSpaceOnUse"
                        >
                          <stop stopColor="#86C4FF" />
                          <stop offset="1" stopColor="#389FFF" />
                        </linearGradient>
                      </defs>
                    </svg>

                    {/* Play Icon */}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="107"
                      height="120"
                      viewBox="0 0 107 120"
                      fill="none"
                      style={{
                        position: "absolute",
                        top: 95,
                        left: 110,
                        opacity: isPlaying ? 0 : 1,
                        transform: isPlaying ? "scale(1.2)" : "scale(1)",
                        transition: "opacity 0.3s ease, transform 0.3s ease",
                      }}
                    >
                      <path
                        d="M0.11697 10.0705C0.116967 2.37251 8.4503 -2.43875 15.117 1.41025L101.367 51.2067C108.034 55.0557 108.034 64.6782 101.367 68.5272L15.117 118.324C8.45031 122.173 0.116969 117.361 0.11697 109.663L0.11697 10.0705Z"
                        fill="url(#paint0_linear_2531_56)"
                      />
                      <defs>
                        <linearGradient
                          id="paint0_linear_2531_56"
                          x1="0.116968"
                          y1="-7.25"
                          x2="58.8624"
                          y2="94.5"
                          gradientUnits="userSpaceOnUse"
                        >
                          <stop stopColor="#86C4FF" />
                          <stop offset="1" stopColor="#389FFF" />
                        </linearGradient>
                      </defs>
                    </svg>
              </div>
              <div className={style["music-guessor-playing-counter"]}>
                {counter}
              </div>
            </div>
          </div>
          <div className={style["music-guessor-top-right-frame"]}>
            <div className={style["music-guessor-meta-data-box"]}>
              <span>스코어보드</span>
              <div className={style["music-guessor-score-board-wrapper"]}>
                {top3Users.map((user, index) => {
                  return <ScoreComponent
                    key={index}
                    index={index}
                    nickname={user.nickname}
                    point={user.point}
                  />
                })
                }
              </div>
            </div>
            <div className={style["music-guessor-meta-data-box"]}>
              <span>답변 내역</span>
              <div className={style["music-guessor-answer-wrapper"]}>
                {
                  sampleChatting.map((answer, index)=>{
                    return <AnswerChattingComponent
                      key={index}
                      answer={answer}
                    />
                  })
                }
              </div>
            </div>
          </div>
        </div>
        <div className={style["music-guessor-bottom-frame"]}>
          <div className={style["music-guessor-input-frame"]}>
            <div className={style["music-guessor-input-wrapper"]}>
              <input
                className={style["music-guessor-input"]}
                value={answer}
                onChange={(e) => {
                  handleInput(e);
                }}
                placeholder={answer? answer: "정답"}
                type="text"
                onKeyDown={handleNewAnswer}
              >
              </input>
            </div>
          </div>
          <div className={style["music-guessor-next-button-frame"]}>
            <div className={style["music-guessor-next-button-wrapper"]}>
              <div className={style["music-guessor-next-button"]}
                onClick={handleShowAnswer}
              >
                <span>다음</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className={style["music-guessor-upper-frame"]}
          style={{
            height: answerFlag ? "70%" : "0%",
            display : answerFlag ? "visible" : "hidden",
            opacity :answerFlag ? 1 : 0,
          }}
        >
          <div id="player"
            style={{
              display : answerFlag ? "visible" : "hidden",
            }}
          ></div>
      </div>
    </div>
  );
}





















//------------------------------------------------------------------------------







function ContentIntroSlide({
  title, howToUse, option, subOption,
  input, setInput, buttonPress
}) {

  const handleNextSlide =() => {
    console.log(setInput)
    if(setInput){
      if (input == ""){
        alert("정답을 입력해주세요!");
        return
      }
    }
    buttonPress()
  };

  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]} >  
      {/*여기부터 천천히 등장해야됨 */}
      <div className={style["content-meta-body"]}>
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
            onClick={()=>{
              handleNextSlide()
            }}
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

