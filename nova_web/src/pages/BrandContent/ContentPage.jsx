import React, { useEffect, useState, useRef, forwardRef } from 'react';
import { CSSTransition, TransitionGroup } from "react-transition-group";
import "./animations.css"; // CSS 애니메이션 정의
import brandStyle from "./../BrandPage/brandPage.module.css";
import style from "./style.module.css";


import chzzkLogo from "./../BrandPage/chzzklogo_kor(Green) 1.png";
import soopLogo from "./../BrandPage/SOOP_LOGO_Blue 1.png";
import contentBackgroundImage from "./content-background-svg.svg";
import bluredBackgroundImage from "./blurBackground.png";
import brandImg from "./brand_img.png";
import mainApi from "../../services/apis/mainApi.js";

import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";
import chzzkApi from '../../services/apis/chzzkApi.js';
import { io, Socket } from "socket.io-client";

export default function ContentPage (){
  const socketRef = useRef(null);

  const [accessToken, setAccessToken] = useState("");
  const [refreshToken, setRefreshToken] = useState("");
  const [tokenType, setTokenType] = useState("Bearer");
  const [expiresIn, setExpiresIn] = useState("");


  const [start, setStart] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [chattings, setChattings] = useState([]);
  const [filteredChatting, setFilteredChatting] = useState([]);
  const [selectedPage, setSelectedPage] = useState(0);
  const [filteredCode, setFilteredCode] = useState("");
  const [sessionURL, setSessionURL] = useState("");
  const filteredCodeRef = useRef(filteredCode);
  const filteredCodes = ['','질문', '좌표', '정답'];

  useEffect(()=>{
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const state = params.get("state");
    const savedState = localStorage.getItem("chzzk_oauth_state")

    if (state !== savedState) {
      console.log("state 검증 실패! 요청이 의심됩니다.");
      return;
    }

    if (code) {
      mainApi.get(`/content_system/try_auth_chzzk?code=${code}&state=${state}`).then((result) => {
        setAccessToken(result.accessToken);
        setRefreshToken(result.refreshToken);
        setTokenType(result.tokenType);
        setExpiresIn(result.expiresIn);
        setSessionURL(result.url)
      });
    }
  }, [])

  const subscribeChzzkChat = async (sessionKey) => {
    mainApi.get(`/content_system/try_subscribe_chat?sessionKey=${sessionKey}`).then((res) => {
      const result = result
    });
  }



  useEffect(() => {
    // 백엔드에서 세션 생성 요청 (유저용)
    const initialization = async () =>{
      try{
        const wsURL = sessionURL.replace(/^http(s?):\/\//, 'wss://');

        const socketOption = {
          reconnection: false,
          'force new connection': true,
          'connect timeout': 3000,
          transports: ['websocket']
        };

        const socket = io.connect(wsURL, socketOption);
 
        socketRef.current = socket;

        // 소켓 연결 성공 시
        socket.on('connect', (event) => {
          console.log(event);
          console.log('✅ WebSocket 연결됨');
          subscribeChzzkChat()
        });

        socket.onmessage = (event) => {
          console.log(event.data);
          const data = { message: event.data, filter: filteredCodeRef.current };
          analyzeMessage(data);
        };
      }
       catch (error) {
        console.error('Error during initialization:', error);
        }
      }

      initialization(); 

    return () => {
      if (socketRef.current) {
          socketRef.current.close();
      }};
    }, [sessionURL]);



  //useEffect(() => {
    //const initialize = async () => {
    //try {

        //// 2. fetchFeedComment 완료 후 WebSocket 초기화
        //const socket = new WebSocket('wss://supernova.io.kr/testing_websocket')
        //socketRef.current = socket;

        //socket.onopen = () => {
        //setConnectionStatus('Connected');
        //};

        //socket.onmessage = (event) => {
          //const data = { message: event.data, filter: filteredCodeRef.current };
          //analyzeMessage(data);
        //};

        //socket.onclose = () => {
        //setConnectionStatus('Disconnected');
        //};

        //socket.onerror = (error) => {
        //console.error('WebSocket error:', error);
        //};
    //} catch (error) {
        //console.error('Error during initialization:', error);
    //}
    //}
    //initialize(); 

    //return () => {
    //if (socketRef.current) {
        //socketRef.current.close();
    //}
    //};

  //}, []); // 필요한 의존성 추가

  useEffect(()=>{
    setFilteredCode(filteredCodes[selectedPage]);
  }, [selectedPage])

  // 최신 값을 ref에 항상 저장
  useEffect(() => {
    filteredCodeRef.current = filteredCode;
  }, [filteredCode]);


  function analyzeMessage(data) {
    const socket = socketRef.current;
    if (!socket) {
      console.error("Socket is not initialized");
      return;
    }

    // ping 처리
    if (data === "ping") {
      socket.send("pong");
      return;
    }

    try {
      // 실제 데이터는 JSON 형식으로 들어옴
      const parsed = typeof data === "string" ? JSON.parse(data) : data;
      const filter = data.filter

      // 기본 구조 확인
      if (parsed.type !== "chat") return;

      const messageData = parsed.data;
      const content = messageData?.message?.content ?? "";
      const userId = messageData?.senderChannelId ?? "";
      const nickname = messageData?.profile?.nickname ?? "닉네임없음";

      const chatObj = {
        _id: chattings.length,
        uid: userId,
        uname: nickname,
        body: content,
      };

      setChattings((prev) => [...prev, chatObj]);

      // 예시 filter 사용
      if (!content.startsWith(filter)) {
        setFilteredChatting((prev) => [...prev, chatObj]);
      }

    } catch (error) {
      console.error("❌ 채팅 메시지 파싱 에러:", error);
    }
  }

  //function analyzeMessage(data) {
    //const message = data.message
    //const filter = data.filter

    //const socket = socketRef.current; // Access the WebSocket instance directly

    //if (!socket) {
      //console.error('Socket is not initialized');
      //return;
    //}

    //if (message === "ping") {
      //socket.send("pong");
      //return;
    //}

    //try {
      //// Parse the message
      //const messageParts = message.split('<br>');
      //// Extract `type` and remove it from parsedMessage
      //const messageType = messageParts[0];


      //const transformedMessage = parseDataToObject(message);
      //console.log(filter);

      //// Handle different message types
      //if (messageType === "add") {
        //setChattings((prev) => [...prev, transformedMessage]);
        //if (!transformedMessage.body.startsWith(filter)) {
          //setFilteredChatting((prev) => [...prev, transformedMessage])
        //}
        ////console.log(transformedMessage)
      //}

    //} catch (error) {
      //console.error('Error parsing message:', error);
    //}
  //}

  //function parseDataToObject(data) {
    //// 데이터를 줄바꿈 단위로 분리
    //const [type, owner, uid, uname, cid, body, date] = data.split('<br>');


    //let booleanValue = owner.toLowerCase() === "true";

    //// 객체 생성 및 반환
    //return {
      //_id: chattings.length,
      //uid: uid, // 유아이디
      //uname: "임시 유저", // 유저 이름
      //body: body, // 본문
    //};
  //}


  return (
    <div className={style["trick-container"]}>
    {start ? (
      <ConnectedComponent 
        chattings={chattings}
        setChattings={setChattings}
        filteredChatting={filteredChatting}
        selectedPage={selectedPage}
        setSelectedPage={setSelectedPage}
      />
    ) : (
      <IntroComponent start={start} setStart={setStart} />
    )}
    </div>
  );
}

function Stopwatch({
  duration,
  triggerSignal,
  onComplete
}) {
  const [timeLeft, setTimeLeft] = useState(duration);
  const animationRef = useRef(null);

  useEffect(() => {
    if (triggerSignal === 0) return; // ❗ 초기값은 무시

    let start = performance.now();

    const frame = (now) => {
      const elapsed = now - start;
      const remaining = duration - elapsed;

      if (remaining > 0) {
        setTimeLeft(remaining);
        animationRef.current = requestAnimationFrame(frame);
      } else {
        setTimeLeft(0); // 종료 시 0
        onComplete?.(true); // ✅ 완료 콜백 호출
      }
    };

    // 이전 애니메이션 정리 후 새로 시작
    if (animationRef.current) cancelAnimationFrame(animationRef.current);
    animationRef.current = requestAnimationFrame(frame);

    return () => cancelAnimationFrame(animationRef.current);
  }, [triggerSignal]);

  return (
    <div className={style["stopwatch-container"]}>
      채팅창 대기 {(timeLeft / 1000).toFixed(1)}초
    </div>
  );
}


function IntroComponent({setStart}){
  const title = "SUPERNOVA 컨텐츠 클럽에 오신걸 환영합니다.";
  const subtitle = "SUPERNOVA 컨텐츠 클럽은 방송 플랫폼에서 실시간 스트리밍을 통해 사용 가능합니다."


  const fetchTest = async () => {
    const clientId = "cd2bbdef-c85b-4f84-8a26-76e5de315e5a";
    const redirectUri = "https://supernova.io.kr/content"; // chzzk에 등록된 URI
    const state = crypto.randomUUID();

    // state 저장 (나중에 콜백에서 검증용)
    localStorage.setItem("chzzk_oauth_state", state);

    // 인증 URL 만들기
    const authUrl = `https://chzzk.naver.com/account-interlock?clientId=${clientId}&redirectUri=${encodeURIComponent(redirectUri)}&state=${state}`;

    // 브라우저를 인증 URL로 이동 (리디렉션)
    window.location.href = authUrl;
  }


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
                    onClick={()=>fetchTest()}
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

function ConnectedComponent({
  chattings, setChattings, filteredChatting,
  selectedPage, setSelectedPage
}) {
  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
  const pageTitle = "닉네임1234님 어서오세요!";
  const subTitle = "화면 오른쪽에서 ㅓ원하는 컨텐츠로 선택하세요!";
  const [duration, setDuration] = useState(0); // 5초

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
            chattings={chattings}
            pages={pages}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
            duration={duration}
            setDuration={setDuration}
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
            chattings={chattings}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
            filteredChatting={filteredChatting}
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
            chattings={chattings}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
            filteredChatting={filteredChatting}
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
            chattings={chattings}
            filteredChatting={filteredChatting}
            selectedPage={selectedPage}
            setSelectedPage={sliderController}
            duration={duration}
          />
        </SwiperSlide>
      </Swiper>
    </div>
  );
}


function WatiingRoomComponent({
  chattings, pages, selectedPage, setSelectedPage,
  duration, setDuration
}){
  const [syncFlag, setSyncFlag] = useState(false);
  const pageTitle = "닉네임1234님 어서오세요!";
  const subTitle = "화면 오른쪽에서 원하는 컨텐츠로 선택하세요!";

  const howToUse = [
    "1. 실제 스트리밍 창 (치지직, SOOP 등)을 크롬을 사용하여 입장합니다.",
    "2. 크롬화면에서 스트리밍 되는 문구를 채팅창에 입력합니다.",
    "3. 채팅창과 실제 스트리머의 화면의 차이를 자동으로 확인합니다.",
    "4. 빠르게 입력 할 수록, 싱크가 정확해집니다."
  ]

  const words = ["사슴", "토끼", "곰", "호랑이", "여우", "늑대", "고양이", "개", "원숭이", "코끼리"];
  const [targetWord, setTargetWord] = useState(words[Math.floor(Math.random() * words.length)]);

  const [elapsedTime, setElapsedTime] = useState(0);

  const startTimeRef = useRef(performance.now()); // 시작 시간 저장용

  // 단어를 바꾸고 타이머 시작
  const changeTargetWord = () => {
    const newWord = words[Math.floor(Math.random() * words.length)];
    setTargetWord(newWord);
    startTimeRef.current = performance.now(); // 시간 초기화
  };

  // 최초 mount 또는 syncFlag가 true일 때 5초 간격으로 단어 변경
  useEffect(() => {
    if (!syncFlag) return;

    startTimeRef.current = performance.now(); // 시간 초기화
    //const interval = setInterval(() => {
      //changeTargetWord();
    //}, 5000);

    //// 시작 시점 초기화
    //changeTargetWord();

    //return () => clearInterval(interval);
  }, [syncFlag]);

  // 채팅이 바뀔 때마다 정답 확인
  useEffect(() => {
    if (chattings.length === 0) return;

    const lastChat = chattings[chattings.length - 1].body;

    if (lastChat === targetWord) {
      const now = performance.now();
      const elapsed = now - startTimeRef.current;

      setDuration(elapsed); // 경과 시간 업데이트
      changeTargetWord(); // 새로운 단어로 변경
    }
  }, [chattings]);


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
    <div className={brandStyle["brand-page-background"]}>
    <div className={style["content-container"]} >
      <div className={style["waiting-room-side-frame"]}>
        <div className={style["sub-tools-wrapper"]}>
          <div className={style["tools-container"]}>
            <div className={style["tools-detail-wrapper"]}>
              <div className={style["tools-title"]} >
                {tools[0].title}
              </div>
              <div className={style["tools-subtitle"]}>
                {tools[0].subtitle}
              </div>
            </div>
            <button className={style["tools-button"]}
              onClick={()=> setSyncFlag(!syncFlag)}
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
              onClick={()=>{
                window.location.reload();
              }}
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
          <div className={style["chatting-wrapper"]}
            style={{backgroundSize: "40%"}}
          >
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
      <div className={style["set-sync-frame-wrapper"]}
          style={{
            display: syncFlag ? "flex" : "none", // 또는 "block"
            opacity :syncFlag? 1 : 0,
          }}
          onClick={()=> setSyncFlag(!syncFlag)}
      >
        <div className={style["set-sync-frame"]} 
          onClick={(e) => e.stopPropagation()}
        >
          <div className={style["content-info-n-how-to-use"]}
            style={{width: "100%", gap: "25px"}}
          >
            <span>
              싱크 맞추기
            </span>
            <div className={style["how-to-use"]}
              style={{display: "flex", flexDirection:"column", gap: "15px"}}
            >
              {
                howToUse.map((usage, index)=>{
                  return <li key={index}>{usage}</li>
                })
              }
            </div>
          </div>
          <div className={style["set-sync-content-frame"]}>
            {targetWord}
          </div>
          <div className={style["set-sync-button-wrapper"]}>
            <div
              onClick={()=>{
                setDuration((prev)=> prev + 1000);
              }}
            >
              +
            </div>
            <span>
              {(duration/ 1000).toFixed(2)}초
            </span>
            <div
              onClick={()=>{
                setDuration((prev)=> prev - 1000);
              }}
            >
              -
            </div>
          </div>
        </div>
      </div>
    </div>
    <img src={bluredBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]} 
      style={{height: "100vh"}}
    />
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

function QuestionGuessorComponent({
  chattings, myIndex, selectedPage,
  setSelectedPage, filteredChatting
}){
  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
  const [isChattingOn, setIsChattingOn] = useState(true);
  const title = "스무고개";
  const howToUse =[
    "1. 스트리머가 주제를 정합니다.",
    "2. 스트리머가 선택한 주제에 시청자가 질문합니다.",
    "3. 스트리머는 대답할 질문을 선택합니다.",
    "4. 스트리머가 질문에 '네', '아니오'로 대답합니다.",
  ];

  const makeItVoid= () => {
    setTarget([""]);
    setSelectedPage(0);
    setNumQuestion(20);
    setTargetIndex(0);
    swiperRef.current?.slideTo(0);
  }

  const [numQuestion, setNumQuestion] = useState(20);

  const option = `남은 질문 ${numQuestion}개`;
  const subOption = "클릭하여 질문 개수 조정하기";

  const [targetIndex, setTargetIndex] = useState(0);
  const [input, setInput] = useState("");
  const [target, setTarget] = useState([""]);

  const handleInput = (e) => {
    const newInput = e.target.value;
    setInput(newInput); // 입력 값을 상태로 설정
  };

  const confirmInput = () => {
    // 최신 슬라이드의 내용을 입력값으로 실시간 업데이트
    setTarget((prev) => {
      const newTarget = [...prev];
      newTarget[newTarget.length - 1] = input;
      return newTarget;
    });
    setInput("");
    sliderController();
  }

  const makeNewSlideController = () => {
    setTarget((prev)=> [...prev, ""]);
    sliderController();
  }

  const bringToNextStage = () =>{
    setTargetIndex((prev) => prev+1);
    sliderController();
  }

  const sliderController = () => {
    swiperRef.current?.slideNext();
  }

  const ReverseSliderController = () =>{
    swiperRef.current?.slidePrev();
  }

  // 슬라이드하면 나타나는 뭐시기 애니메이션인데 이거 필요없을듯
  const handlePage = (e) => {
    executeSlideAnimation();
  }


  return(
    <div className={brandStyle["brand-page-background"]}>
    <div className={style["content-container"]}
      style={{flexDirection:"column"}}
    >
      <div className={brandStyle["topBar-frame"]}>
        <div className={brandStyle["topBar-div"]}>
          <div className={brandStyle["topBar-text-wrapper"]}
            style={{width: "auto", marginTop:"20px", marginBottom: "20px"}}
            onClick={makeItVoid}
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
              {
                isChattingOn ? (
                  <div className={style["chatting-wrapper"]}>
                  {
                    filteredChatting.map((chatting, index) =>{
                      return (
                          <Chatting key={chatting} index={index} body={chatting.body}/>
                      );
                    })
                  }
                  </div>
                ) : (
                  <div className={style["chatting-cover"]}>
                  </div>
                )
              }
              <ToggleSwitch id="chatToggle1" isChecked={isChattingOn} setIsChecked={setIsChattingOn}/>
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
          {
            target.map((question, index) => {
              return (
                index === targetIndex ? (
                  <React.Fragment key={index}>
                    <SwiperSlide key={`intro-${index}`}>
                      <ContentIntroSlide 
                        title={title}
                        howToUse={howToUse}
                        numQuestion={numQuestion}
                        setNumQuestion={setNumQuestion}
                        option={option}
                        subOption={subOption}
                        input={input}
                        setInput={handleInput}
                        buttonPress={confirmInput}
                      />
                    </SwiperSlide>
                    <SwiperSlide key={`playing-${index}`}>
                        <QuestionGuessorPlayingSlide 
                          initNumQuestion={numQuestion}
                          buttonPress={makeNewSlideController}
                          chattings={chattings}
                        />
                    </SwiperSlide>
                    <SwiperSlide key={`clear-${index}`}>
                        <QuestionGuessorClearSlide 
                          title={title}
                          howToUse={howToUse}
                          initNumQuestion={numQuestion}
                          option={option}
                          subOption={subOption}
                          input={question}
                          setInput={handleInput}
                          buttonPress1={bringToNextStage}
                          buttonPress2={ReverseSliderController}
                        />
                    </SwiperSlide>
                  </React.Fragment>
                ):(
                  <React.Fragment key={index}>
                    <SwiperSlide key={`trash-1-${index}`}>
                      <TrashComponent />
                    </SwiperSlide>
                    <SwiperSlide key={`trash-2-${index}`}>
                      <TrashComponent />
                    </SwiperSlide>
                    <SwiperSlide key={`trash-3-${index}`}>
                      <TrashComponent />
                    </SwiperSlide>
                  </React.Fragment>
                )
              );
            })
          }
        </Swiper>
      </div>
    </div>
    <img src={bluredBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]}
      style={{height: "100vh"}}
    />
    </div>
  );
}


function QuestionGuessorPlayingSlide({
  buttonPress, initNumQuestion, chattings
}){
  const refs1 = useRef([]); // ref 배열을 한 번만 생성
  const refs2 = useRef([]); // ref 배열을 한 번만 생성
  const [waitingQuestion, setWaitingQuestion] = useState([]);
  const [answeredQuestion, setAnsweredQuestion] = useState([]);
  const [fade, setFade] = useState("fade-in");
  const [numQuestion, setNumQuestion] = useState(initNumQuestion);

  useEffect(() => {
    setNumQuestion(initNumQuestion);
  }, [initNumQuestion])

  useEffect(() => {
    if (chattings.length > 0) {
      const lastChat = chattings[chattings.length - 1].body;
      //const targetUser = chattings[chattings.length - 1].uname;
      
      if (waitingQuestion.length < 3){
        if (lastChat.startsWith('질문')) {

          // "정답" 뒤의 내용을 처리
          const answerContent = lastChat.slice(3).trim(); // "정답" 뒤의 문자열 추출
          const now = new Date();
          const id = `id_${now.getFullYear()}${now.getMonth() + 1}${now.getDate()}${now.getHours()}${now.getMinutes()}${now.getSeconds()}`;

          const newChatting = {
            id: id,
            answer: 0,
            body: answerContent,
          };
      
          // 추가 로직 실행
          if (answerContent) {
            setWaitingQuestion((prev)=>[...prev, newChatting]);
          }
        }
      }
    }
  }, [chattings]);


  // 렌더링 전에 배열 크기 맞춰주기
  useEffect(() => {
    refs1.current = waitingQuestion.map((_, i) => refs1.current[i] || React.createRef());
  }, [waitingQuestion]);

  // 렌더링 전에 배열 크기 맞춰주기
  useEffect(() => {
    refs2.current = waitingQuestion.map((_, i) => refs2.current[i] || React.createRef());
    setNumQuestion(initNumQuestion - answeredQuestion.length)
  }, [waitingQuestion]);

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
              {waitingQuestion.map((question, index) => {
                return(
                <CSSTransition
                  key={index}
                  timeout={300}
                  classNames="fade"
                  nodeRef={refs1.current[index]}
                >
                  <QuestionObject
                    nodeRef={refs1.current[index]}
                    question={question}
                    waitingQuestion={waitingQuestion}
                    remainQuestion={numQuestion}
                    setWaitingQuestion={setWaitingQuestion}
                    setAnsweredQuestion={setAnsweredQuestion}
                  />
                </CSSTransition>
                );
              })}
            </TransitionGroup>
          </div>
          <div className={style["question-guessor-top-right-wrapper"]}>
            <div className={style["stage-meta-data-box"]}>
              <span
                className={style[`question-text ${fade}`]}
                style={{color:"#111", fontSize:"36px", height:"50px"}}>
                남은 질문 {numQuestion}개
              </span>
            </div>
            <div className={style["stage-meta-data-box"]}>
              <img src={brandImg} className={style["brand-image"]}/>
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
                nodeRef={refs2.current[index]}
              >
                <QuestionObject
                  nodeRef={refs2.current[index]}
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
  buttonPress1, buttonPress2, input
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
              {input}
            </span>
          </div>
          <div className={style["question-guessor-clear-button-wrapper"]}>
            <div className={style["content-meta-frame-input-wrapper2"]}
              onClick={()=>{buttonPress2()}}
            >
              <span 
              >
               이전으로
              </span>
            </div>
            <div className={style["content-meta-frame-input-wrapper2"]}
              onClick={()=>{buttonPress1()}}
            >
              <span 
              >
                다시 시작
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const QuestionObject = forwardRef(function QuestionObject({
   question, waitingQuestion, remainQuestion,
  setWaitingQuestion, setAnsweredQuestion },
  nodeRef
){
  const [isClicked, setIsClicked] = useState(false);
  const [isFading, setIsFading] = useState(false);
  const s_answer = ["네", "아니오", "거절"];

  const handleClick = () => {
    setIsClicked((prev) => !prev);
  };

  const handleAnswer = (index) => {
    setIsFading(true); // 페이드 아웃 시작
    if (remainQuestion <= 0 && index !== 3){
      alert("질문 갯수를 초과 했습니다.");
      return;
    };

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
        ref={nodeRef}
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
        ref={nodeRef}
      >
        <div className={style["question-object-body"]}
            style={{
              border : isClicked ? "1px solid #111" : "1px solid #5C5C5C",
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
});



//----------------------------------------------------------













function DiffGuessorComponent({
  chattings, selectedPage, myIndex, setSelectedPage,
  filteredChatting
}){
  const diffSwiperRef= useRef(null);
  const [isChattingOn, setIsChattingOn] = useState(true);
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
    <div className={brandStyle["brand-page-background"]}>
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
              {
                isChattingOn ? (
                  <div className={style["chatting-wrapper"]}>
                  {
                    filteredChatting.map((chatting, index) =>{
                      return (
                          <Chatting key={index} index={index} body={chatting.body}/>
                      );
                    })
                  }
                  </div>
                ) : (
                  <div className={style["chatting-cover"]}>
                  </div>
                )
              }
              <ToggleSwitch id="chatToggle2" isChecked={isChattingOn} setIsChecked={setIsChattingOn}/>
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
            <ContentIntroSlide1 
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
    <img src={bluredBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]}
      style={{height: "100vh"}}
    />
    </div>
  );
}



//-------------------------------------------------------------------------------------------










function MusicGuessorComponent({
  chattings, myIndex, selectedPage, setSelectedPage,
   filteredChatting, duration
}){
  const diffSwiperRef= useRef(null);
  const defaultOptions = {"전체" : 0}
  const [isChattingOn, setIsChattingOn] = useState(true);
  const [selectedOption, setSelectedOption] = useState("전체");

  const [optionList, setOptionList] = useState(defaultOptions);
  const [numMusic, setNumMusic] = useState(0);


  const content = []
  const tempUser = [
    //{ id: 0, uname: "가짜 이름 1", point: 10 },
  ];

  const tempChatting = [
    //{ id: 4, body: "이건 뭐지", state:false},
    //{ id: 0, body: "정답!", state:false },
    //{ id: 1, body: "잠시만 저거", state:false},
    //{ id: 2, body: "이게정답임", state:true},
  ]


  const[contents, setContents] = useState(content);
  const[activeIndex, setActiveIndex] = useState(-1);


  const [answers, setAnswers] = useState(tempChatting);

  const [userList, setUserList] = useState(tempUser);
  const [top3Users, setTop3Users] = useState([]);

  const makeItVoid = () => {
    setSelectedPage(0);
    setActiveIndex(-1);
    setContents(content);
    setUserList(tempUser);
    setTop3Users([]);
    diffSwiperRef.current?.slideTo(0);
  }

  const title = "뮤직게서";
  const howToUse =[
    "1. 노래 듣고 정답을 맞추는 컨텐츠입니다.",
    "2. 시청자는 채팅창에 정답을 입력합니다.",
    "3. 예시: 정답 노래이름",
    "4. 스트리머는 화면 하단에 정답을 입력합니다.",
  ];

  const subTitle = '인트로 15초 듣기';

  const handleSlide = () => {
    diffSwiperRef.current?.slideNext()
    setActiveIndex((prev)=>prev+1)
  };

  const tryStartContent = async () => {
    await fetchContentData();
    handleSlide();
  }


  const resetData = () => {
    diffSwiperRef.current?.slideTo(0)
    setActiveIndex(-1);
    setContents(content);
    setUserList(tempUser);
    setTop3Users([]);
  }

  const handleUserList = (chatting) => {
    // userList는 기존 유저 리스트 상태라고 가정
    setUserList((prevList) => {
      const existingUserIndex = prevList.findIndex(
        (user) => user.uname === chatting.uname
      );

      if (existingUserIndex !== -1) {
        // 기존 유저인 경우: 포인트 증가
        const updatedList = [...prevList];
        updatedList[existingUserIndex].point += 1;
        return updatedList;
      } else {
        // 새 유저인 경우: 새 유저 추가
        const newId = prevList.length > 0
          ? Math.max(...prevList.map((u) => u.id)) + 1
          : 0;
        return [
          ...prevList,
          {
            id: newId,
            uname: chatting.uname,
            point: 1,
          },
        ];
      }
    });
  };

  const fetchMetaData = () => {
    mainApi.get('/content_system/get_num_music_content').then((res) => {
      const meta_data = res.data.body.meta_data
      setOptionList(meta_data)
    });
  }

  const fetchContentData = async () => {
    mainApi.get(`/content_system/get_music_content?type=${selectedOption}&num_content=${numMusic}`).then((res) => {
      const content = res.data.body.content
      setContents(content)
    });
  }

  useEffect(()=> {
    fetchMetaData()
  }, [])


  useEffect(() => {
    if (userList) {
      // point 기준으로 내림차순 정렬 후 상위 3명만 선택
      const sortedTop3 = [...userList]
        .sort((a, b) => b.point - a.point)
        .slice(0, 3);
      setTop3Users(sortedTop3);
    }
  }, [userList]); // userList가 변경될 때 실행


  return(
    <div className={brandStyle["brand-page-background"]}>
    <div className={style["content-container"]}
      style={{flexDirection:"column"}}
    >
      <div className={brandStyle["topBar-frame"]}>
        <div className={brandStyle["topBar-div"]}>
          <div className={brandStyle["topBar-text-wrapper"]}
            style={{width: "auto", marginTop:"20px", marginBottom: "20px"}}
            onClick={()=>{
              makeItVoid();
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
              {
                isChattingOn ? (
                  <div className={style["chatting-wrapper"]}>
                  {
                    filteredChatting.map((chatting, index) =>{
                      return (
                          <Chatting key={index} index={index} body={chatting.body}/>
                      );
                    })
                  }
                  </div>
                ) : (
                  <div className={style["chatting-cover"]}>
                  </div>
                )
              }
              <ToggleSwitch id="chatToggle3" isChecked={isChattingOn} setIsChecked={setIsChattingOn}/>
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
            <ContentIntroSlide2 
              optionList = {optionList}
              subTitle ={subTitle}
              buttonPress={tryStartContent}
              selectedOption={selectedOption}
              setSelectedOption={setSelectedOption}
              numMusic={numMusic}
              setNumMusic={setNumMusic}
            />
          </SwiperSlide>
          {
            contents.map((content, index)=>{
              return(
                <SwiperSlide
                  key={index}
                >
                  { 
                  activeIndex == index ? (
                    <MusicGuessorPlayingSlide
                      content={content}
                      top3Users={top3Users}
                      buttonPress={handleSlide}
                      answers={answers}
                      setAnswers={setAnswers}
                      chattings={chattings}
                      handleUserList={handleUserList}
                      duration={duration}
                    />
                  ):(
                    <TrashComponent
                      key={index}
                    />
                  )
                  }
                </SwiperSlide>
              )
            })}
            <SwiperSlide>
              <MusicGuessorClearSlide
                buttonPress={resetData}
                userList={userList}
              />
            </SwiperSlide>
        </Swiper>
      </div>
    </div>
    <img src={bluredBackgroundImage} alt="Brand Highlight" className={brandStyle["brand-highlight-background-image"]}
      style={{height: "100vh"}}
    />
    </div>
  );
}

function TrashComponent(){
  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]} 
      style={{justifyContent:"center", alignItems:"center", opacity:1, position:"relative"}}
    >  
    </div>
  );
}



function MusicGuessorPlayingSlide({
  client, handleUserList,
  content, buttonPress, top3Users,
  answers, setAnswers, chattings,
  duration
}){

  const playerRef = useRef(null);
  const [answerFlag, setAnswerFlag] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [stopwatchSwitch, setStopwatchSwitch] = useState(false);
  const [syncFlag, setSyncFlag] = useState(false);

  const handleShowAnswer =()=>{
    if (!answerFlag){
      setAnswerFlag(true);
    }
    setModalOpen((prev)=>!prev);
  }

  useEffect(() => {
    const playerId = `youtube-player-${content.url}`;

    const initializePlayer = () => {
      if (!document.getElementById(playerId)) {
        console.error(`Player container with id ${playerId} does not exist.`);
        return;
      }

      playerRef.current = new window.YT.Player(playerId, {
        height: '70%',
        videoId: content.url,
        playerVars: {
          autoplay: 0,
          controls: 1,
          playsinline: 1,
        },
      });
    };

    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      window.onYouTubeIframeAPIReady = initializePlayer;
    } else {
      initializePlayer();
    }

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
      }
    };
  }, [content.url]);

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
  const [trigger, setTrigger] = useState(0);


  const handleMyAnswer = (e) =>{
    if (e.key === 'Enter') {
      setTrigger(Date.now());
    }
  }

  useEffect(() => {
    if(syncFlag){
      const now = new Date();
      const id = `id_${now.getFullYear()}${now.getMonth() + 1}${now.getDate()}${now.getHours()}${now.getMinutes()}${now.getSeconds()}`;
      const newChatting = {
        id: id,
        uname: "클라이언트", //유저 이름이 들어감
        body: answer,
        state: false
      };
      
      const normalizedAnswer = answer.replace(/\s/g, ""); // 공백 모두 제거

      // content.name 배열도 각각 공백 제거해서 비교

      if (content.answer.includes(normalizedAnswer)) {
        newChatting.state = true
        if (!answerFlag){
          handleUserList(newChatting);
        }
        setAnswerFlag(true);
      }

      setAnswers((prev)=>[...prev, newChatting]);
      setAnswer("");
      setSyncFlag(false);
    }
  },[syncFlag]);


  useEffect(() => {
    if (chattings.length > 0) {
      const lastChat = chattings[chattings.length - 1].body;
      const targetUser = chattings[chattings.length - 1].uname;

      if (lastChat.startsWith('정답')) {

        // "정답" 뒤의 내용을 처리
        const answerContent = lastChat.slice(3).trim(); // "정답" 뒤의 문자열 추출
        const now = new Date();
        const id = `id_${now.getFullYear()}${now.getMonth() + 1}${now.getDate()}${now.getHours()}${now.getMinutes()}${now.getSeconds()}`;

        const newChatting = {
          id: id,
          uname: targetUser,
          body: answerContent,
          state: false
        };
      
        if (answerContent) {
          const normalizedAnswer = answerContent.replace(/\s/g, ""); // 공백 모두 제거

          // content.name 배열도 각각 공백 제거해서 비교

          if (content.answer.includes(normalizedAnswer)) {
            newChatting.state = true;
            if (!answerFlag) {
              handleUserList(newChatting);
            }
            setAnswerFlag(true);
          }

          setAnswers((prev) => [...prev, newChatting]);
        }
      }
    }
  }, [chattings]);

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
                {
                  top3Users.map((user, index) => {
                    return <ScoreComponent
                      key={index}
                      index={index}
                      nickname={user.uname}
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
                  answers.map((answer, index)=>{
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
                onKeyDown={handleMyAnswer}
              >
              </input>
            </div>
            <Stopwatch
              duration={duration}
              triggerSignal={trigger}
              onComplete={setSyncFlag}
            />
          </div>
          <div className={style["music-guessor-next-button-frame"]}>
            <div className={style["music-guessor-next-button-wrapper"]}>
              {
                answerFlag && (
                  <div className={style["music-guessor-next-button"]}
                    onClick={buttonPress}
                  >
                    <span
                      style={{
                        color: "#111"
                      }}
                    >다음 문제</span>
                  </div>
                )
              }
              <div className={style["music-guessor-next-button"]}
                onClick={handleShowAnswer}
              >
                <span>정답 보기</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className={style["set-sync-frame-wrapper"]}
        style={{
          backgroundColor: "rgba(0, 0, 0, 0.0)",
          display: modalOpen? "flex" : "none", // 또는 "block"
          opacity : modalOpen? 1 : 0,
        }}
        onClick={()=> setModalOpen(!modalOpen)}
      >
        <div className={style["music-guessor-upper-frame"]}
            onClick={(e) => e.stopPropagation()}
        >
            <span>정답 : {content.title} - {content.artist}</span>
            <div id={`youtube-player-${content.url}`}
              style={{
                display : modalOpen? "visible" : "hidden",
              }}
            ></div>
            <p>Youtube Iframe Player API를 이용한 영상 및 오디오 재생 기능입니다.</p>
        </div>
      </div>
    </div>
  );
}


const ScoreComponent = ({index, nickname, point}) => {
  const colorSample = ["#FFA347", "#479DFF", "#A947FF"];
  const color = colorSample[index];

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





function MusicGuessorClearSlide({
  buttonPress, userList
}){
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
        <div className={style["music-guessor-top-right-frame"]}
          style={{alignItems:"center"}}
          
        >
          <span
            style={{fontSize:"40px", marginBottom:"40px"}}
          >수고하셨습니다.</span>

          <div className={style["music-guessor-meta-data-box"]} >
            <span>스코어보드</span>
            <div className={style["music-guessor-score-board-wrapper"]}
              style={{overflowY:"auto", maxHeight:"100%"}}
            >
              {
                userList.map((user, index) => {
                  return <ScoreComponent
                    key={index}
                    index={index}
                    nickname={user.uname}
                    point={user.point}
                  />
                })
              }
            </div>
          </div>
        </div>
            
        <div className={style["music-guessor-next-button-frame"]}>
          <div className={style["music-guessor-next-button-wrapper"]}
              style={{justifyContent:"center"}}
          >
            <div className={style["music-guessor-next-button"]}
              onClick={buttonPress}
            >
              <span
                style={{
                  color: "#111"
                }}
              >초기화</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}













//------------------------------------------------------------------------------

function ContentIntroSlide({
  title, howToUse, option, subOption, numQuestion, setNumQuestion,
  input, setInput, buttonPress
}) {

  const handleNextSlide =() => {
    if(setInput){
      if (input == ""){
        alert("정답을 입력해주세요!");
        return
      }
    }
    buttonPress();
  };

  const handleIncreaseQuestion = () => {
    if (numQuestion >= 40) {
      alert("질문 갯수는 40개를 초과할 수 없습니다.");
      return;
    }else{
      setNumQuestion((prev)=>prev+1);
    }
  }

  const handleDecreaseQuestion = () => {
    if (numQuestion <= 1) {
      alert("질문 갯수는 1개 이상이어야 합니다.");
    }else{
      setNumQuestion((prev)=>prev-1);
    }
  }


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
            <div className={style["question-meta-data-button-wrapper"]}>
              <div className={style["question-meta-data-button"]}
                onClick={handleIncreaseQuestion}
              >
                +
              </div>
              <div className={style["question-meta-data-button"]}
                onClick={handleDecreaseQuestion}
              >
                -
              </div>
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
              handleNextSlide();
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





function ContentIntroSlide1({
  title, howToUse, option, subOption,
  input, setInput, buttonPress
}) {

  const handleNextSlide =() => {
    if(setInput){
      if (input == ""){
        alert("정답을 입력해주세요!");
        return;
      }
    }
    buttonPress();
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
              handleNextSlide();
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

function ContentIntroSlide2({
  subTitle, optionList, selectedOption, setSelectedOption,
  numMusic, setNumMusic, buttonPress
}) {

  const handleNextSlide =() => {
    buttonPress()
  };

  const increaseNumMusic = (size) => {
    if ((numMusic+size) >= optionList[selectedOption]){
      alert(`해당 장르는 ${optionList[selectedOption]}개를 넘을 수 없습니다.`);
    }else{
      setNumMusic((prev) => prev+size);
    }
  }
  const decreaseNumMusic = (size) => {
    if ((numMusic-size) < 1){
      alert("문제는 1개 이상이어야 합니다!");
    }else{
      setNumMusic((prev) => prev-size);
    }
  }

  useEffect(()=>{
    setNumMusic(optionList[selectedOption]);
  }, [selectedOption])

  useEffect(()=>{
    setNumMusic(optionList[selectedOption]);
  }, [optionList])


  return(
    <div id={"inner-content-id"} className={style["content-container-inner-wrapper"]} >  
      {/*여기부터 천천히 등장해야됨 */}
      <div className={style["content-meta-body"]}>
        <div className={style["content-meta-frame"]}>
          <div className={style["content-meta-data-wrapper"]}>
            <div className={style["meta-data-clickable-div"]}> 
              <span>
                {subTitle}
              </span>
            </div>
          </div>
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
        <div className={style["content-option-selector-wrapper"]}>
          {
          Object.entries(optionList).map(([key, value]) => {
            return (
              <React.Fragment key={key}>
                <div
                  key={key}
                  className={`${style["content-option-selector-container"]} ${
                    selectedOption === key? style["selected"] : ""
                  }`}
                  onClick={() => setSelectedOption(key)}
                >
                  <span>{key}</span>
                  {
                    selectedOption == key ? (
                      <p>{numMusic} 개</p>
                    ):(
                      <p>{value} 개</p>
                    )
                  }
                </div>
                {
                  selectedOption === key &&(
                    <div className={style["content-option-selector-button-wrapper"]}>
                      <div className={style["music-num-raise-button"]}
                        onClick={()=>increaseNumMusic(10)}
                      >
                        +10
                      </div>
                      <div className={style["music-num-raise-button"]}
                        onClick={()=>increaseNumMusic(1)}
                      >
                        +1
                      </div>
                      <div className={style["music-num-raise-button"]}
                        onClick={()=>decreaseNumMusic(1)}
                      >
                        -1
                      </div>
                      <div className={style["music-num-raise-button"]}
                        onClick={()=>decreaseNumMusic(10)}
                      >
                        -10
                      </div>
                    </div>
                  )
                }
              </React.Fragment>
          )})}
        </div>
      </div>
    </div>
  );
}

function ToggleSwitch({id, isChecked, setIsChecked}) {
  const handleToggle = (e) => {
    console.log("Toggle Switch Changed:", e.target.checked);
    setIsChecked(e.target.checked);
  };

  return (
    <div className={style["toggleSwitchWrapper"]}>
      <span>명령어를 제외한 채팅만 표시됩니다.</span>

      <input
        type="checkbox"
        id={id}
        hidden
        checked={isChecked}
        onChange={handleToggle}
      />
      <label htmlFor={id} className={style["toggleSwitch"]}>
        <span className={style["toggleButton"]}></span>
      </label>
    </div>
  );
}