import { useNavigate } from "react-router-dom";
import React, { useEffect, useState, useRef } from "react";
// Swiper 관련 모듈
import { Swiper, SwiperSlide } from "swiper/react";

import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

import style from "./ScheduleMakePage.module.css"; // CSS 모듈 임포트


import HEADER from "../../constant/header";
import mainApi from "../../services/apis/mainApi";
import postApi from "../../services/apis/postApi";

import useBiasStore from "../../stores/BiasStore/useBiasStore";
import ScheduleSelect from "../../component/ScheduleSelect/ScheduleSelect";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import ScheduleCard from "../../component/EventCard/EventCard";
// import required modules

import right_double_arrow from "../../img/right_double_arrow.svg";
import { BIAS_URL, REQUEST_URL } from "../../constant/biasUrl.js";
import tempBias from "../../img/tempBias.png";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";

const textContentList = [
    "새로운 일정을 등록할 목표 주제를 정해주세요!",
    "이미 등록된 일정을 미리 확인해보세요!",
    "일정의 상세 정보를 입력해주세요!",
    "입력한 일정을 검토하여 마무리하세요!"
]


const ScheduleMakeComponent = ({ schedule, index, setSendScheduleData, sendScheduleData }) => {
    const [opacity, setOpacity] = useState(0);

    useEffect(() => {
        const timer = setTimeout(() => {
            setOpacity(1); // 애니메이션으로 나타나게 함
        }, 100); // 약간의 딜레이 추가
        return () => clearTimeout(timer); // 컴포넌트 언마운트 시 타이머 정리
    }, []);

    return (
        <div
            id="input-slide-new-schedule"
            style={{ opacity, transition: "opacity 1s" }}
        >
            <div className={style["input-slide-info"]}>
                <span>이름이 없는 일정은 등록되지 않아요!</span>
            </div>
            <ScheduleSelect
                key={schedule.id}
                index={index}
                setSendScheduleData={setSendScheduleData}
                sendScheduleData={sendScheduleData}
            />
            <div className={style["input-slide-bottom-guide"]}>
                <span>옆으로 밀어 더 추가하기</span>
                <img src={right_double_arrow} alt="arrow-right" />
            </div>
        </div>
    );
};

const ScheduleMakeTitleComponent = () => {
    return (
        <div id="input-slide-new-schedule-title" className={style["input-slide-new-schedule-title"]}>
            <span className={style["title-span"]}>
                새로운 일정을 추가합니다.
            </span>
            <span>
                사용하지 않는 일정은 이름을 비워두세요.
            </span>
        </div>
    );
};

const ScheduleMakeSlideComponent = ({ activeIndex, index,
        schedule,
        setSendScheduleData,
        sendScheduleData
        }) => {
    const [animationFlag, setAnimationFlag] = useState(false);

    const executeMakeNewScheduleAnimation = () => {
        const titleElement = document.getElementById("input-slide-new-schedule-title");
        titleElement.style.opacity = 1; // 반드시 보이게 설정

        if (titleElement) {
            // 애니메이션 시작
            titleElement.style.opacity = 0; // 투명하게 만듦

            setTimeout(() => {
                // 애니메이션이 끝난 후 상태 변경
                setAnimationFlag(true);
            }, 300); // 1초 후 다음 상태로 전환
        }
    };

    useEffect(() => {
        if (activeIndex === index+1) {
            setTimeout(() => {
                executeMakeNewScheduleAnimation();
            }, 300);
        }
        else {
            const titleElement = document.getElementById("input-slide-new-schedule-title");
            titleElement.style.opacity = 1; // 투명하게 만듦
            setTimeout(() => {
            }, 300);
        }

    }, [activeIndex, index]); // activeIndex와 index가 변경될 때 실행

    return animationFlag ?  <ScheduleMakeComponent 
        schedule={schedule}
        index={index+1}
        setSendScheduleData={setSendScheduleData} 
        sendScheduleData={sendScheduleData}
    /> : <ScheduleMakeTitleComponent /> ;
};

const ScheduleMakePage = () => {
    const isMobile = useMediaQuery('(max-width:1100px)');
    const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
    const inputSwiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
    const navigate = useNavigate();

    const [numSchedule, setNumSchedule] = useState(1);
    const [activeIndex, setActiveIndex] = useState(0);
    const [makeScheduleList, setMakeScheduleList] = useState([])

    const scheduleFormat = {
      id: Date.now(), 
      sname : '',
      location : '',
      bid : '',
      start_date : '',
      start_time : '',
      end_date : '',
      end_time : ''
    }

    const [scheduleArray, setScheduleArray] = useState([scheduleFormat]);

    const bundleFormat = {
      sname : '',
      bid : '',
      schedules : scheduleArray
    }

    const biasFormat= {
      bid : "",
      bname : "선택된 주제",
    }

    const [addMode, setAddMode] = useState('single');
    const [tempScheduleData, setTempScheduleData] = useState(bundleFormat)
    const [sendScheduleData, setSendScheduleData] = useState(bundleFormat)
    const [makedScheduleData, setMakedScheduleData] = useState([])

    // 추천 주제 데이터 받기
    async function fetchFormattedScheduleData(scheduleData) {
        await postApi.post("time_table_server/get_schedule_printed_form", {
        header: HEADER,
        body: scheduleData,
        })
        .then((res) => {
        setMakedScheduleData( res.data.body.schedules)})
    }

    async function makeSendScheduleData() {
        let numSchedule = 0;
        const updatedSchedules = tempScheduleData.schedules.filter((element) => {
            if (element.sname !== "") {
                numSchedule += 1;
                return true;
            }
            return false;
        });

        const newSendScheduleData = {
            ...sendScheduleData,
            schedules: updatedSchedules,
        };

        setSendScheduleData(newSendScheduleData); // 상태 업데이트
        if (numSchedule === 1) {
            setAddMode("single");
        } else if (numSchedule > 1) {
            setAddMode("bundle");
        } else {
            setAddMode("error");
        }

        await fetchFormattedScheduleData(newSendScheduleData);
    }



    //let { biasList } = useBiasStore();
    let [ biasList, setBiasList ] = useState([]);
    let [targetBias, setTargetBias] = useState(biasFormat);




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
                    }, 300); // titleBox와 title 애니메이션이 끝난 후 실행
                }, 200); // subtitle 사라지는 애니메이션 시간
            }, 300); // 1초 후 애니메이션 시작
        }
    };




    // 슬라이드 변경 시 애니메이션 실행
    const handleSlideChange = () => {
        const currentIndex = swiperRef.current?.activeIndex;
        const slideId = `swiperSlide${currentIndex}`; // 슬라이드 ID 계산

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

        if (currentIndex === 4){

        }
    };

    useEffect(() => {
        //const currentIndex = swiperRef.current?.activeIndex;
        //const slideId = `swiperSlide${currentIndex}`; // 슬라이드 ID 계산

        const timer = setTimeout(() => {
            swiperRef.current?.slideNext(); // 다음 슬라이드로 이동
        }, 1000); // 1초 대기

        //        setTimeout(() => {
            //console.log(slideId);
            //executeSlideAnimation(slideId);
        //}, 1000)

        setMakeScheduleList([
            { id: Date.now(), index: -1},
            { id: Date.now()+1, index: 0},
        ]);

        //const timer = setTimeout(() => {
            //// Swiper 인스턴스의 slideTo 메서드로 다음 슬라이드로 이동
            //swiperRef.current?.slideTo(1);
        //}, 1000); // 1초 후 슬라이드 이동

        //return () => clearTimeout(timer); // 타이머 정리

    }, []);



    
    // --------------------------------------------------------------------------------------------
    // ---------------------------------   로직 ----------------------------------------------------

  // 추천 주제 데이터 받기
  function fetchBiasData() {
    mainApi.get("time_table_server/get_following_bias_printed_form").then((res) => {
      setBiasList(res.data.body.biases);
    }).catch((error) => {
        if (error.response.status === 401){
            alert("로그인이 필요합니다.");
            navigate("/novalogin");
        }
    })
    ;
  }


  const [searchedSchedule, setSearchedSchedule] = useState([]);

  function fetchSearchSchedule() {
    mainApi.get(`time_table_server/try_search_schedule_with_keyword?search_columns=bname&type=schedule&keyword=${targetBias.bname}`).then((res) => {
      setSearchedSchedule(res.data.body.schedules);
    });
  }


  // 단일 스케줄 만들기
  async function fetchTryMakeSingleSchedule() {

    sendScheduleData.schedules[0].bid = targetBias.bid

    await postApi.post("time_table_server/try_make_new_single_schedule", {
      header: HEADER,
      body: sendScheduleData.schedules[0],
    });
  }

  // 번들 스케줄 만들기
  async function fetchTryMakeBundleSchedule() {
    sendScheduleData.bid = targetBias.bid;

    await postApi.post("time_table_server/try_make_new_multiple_schedule", {
      header: HEADER,
      body: sendScheduleData,
    });
  }

  // 전송하는 함수 (모드를 보고 번들로 보낼지 싱글로 보낼지 확인)
  function tryFetchMakeSchedule(){
    if (addMode == 'single') {
      fetchTryMakeSingleSchedule()
    }
    else if (addMode == 'bundle'){
      fetchTryMakeBundleSchedule()
    }
    else{
        alert("일정이 비어있어요!")
        swiperRef.current?.slidePrev()
    }

  }

  const addSchedule = () => {
    setNumSchedule((prev) => prev + 1);
    const newSchedule = { ...scheduleFormat, id: Date.now() };
    const updatedSchedules = [...tempScheduleData.schedules, newSchedule];
    setTempScheduleData((prev) => ({
      ...prev,
      schedules: updatedSchedules,
    }));
  };


  useEffect(()=>{
    if(numSchedule == 1){
      setAddMode("single")
    }
    else{
      setAddMode("bundle")
    }
  }, [numSchedule])

  useEffect(()=>{
    setTempScheduleData(prevState => ({
      ...prevState,
      bid: targetBias.bid, // bundleNameInput 값으로 sname 업데이트
    }));
  }, [targetBias.bid])


  useEffect( () => {
    // 스케줄 초기화
    setScheduleArray([scheduleFormat]);


    // 추가 모드 설정
    setAddMode('single');
    setNumSchedule(1);

    fetchBiasData(); // 추천 주제 데이터 가져오기
    // 전송 데이터 초기화
    setTempScheduleData(bundleFormat);
  }, [])

  // 슬라이드 변경 시 실행
  const handleMakeNewSchedule = () => {
      const currentIndex = inputSwiperRef.current?.activeIndex;

      if (currentIndex === numSchedule) {
          addSchedule();
          setMakeScheduleList((prev) => [
              ...prev,
              { id: Date.now(), index: currentIndex },
          ]);
      }
      setActiveIndex(currentIndex);
  };


  const handleSelectBias = (index) => {
    const selectedBias = biasList[index];
    setTargetBias(selectedBias); // 선택된 주제 설정

    setTempScheduleData((prevState) => ({
      ...prevState,
      bid: selectedBias.bid, // bundleNameInput 값으로 sname 업데이
    }));
  }

  if(isMobile){
    return (
        <div className="container">
            <div className={style["body-container"]} >
                <Swiper 
                    style={{width: "100%", height: "100%"}}
                    direction={'vertical'}
                    onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
                    onSlideChange={handleSlideChange} // 슬라이드 변경 이벤트
                    speed={1000} // 슬라이드 전환 속도 1초
                    allowTouchMove={false}
                    touchEventsTarget="wrapper"
                >
                    <SwiperSlide>
                        <div id="swiperSlide0" className={style["swiper-slide"]}>
                            <div id ="slideTitleBox" className={style["slide-title-box"]}>
                                <span id="slideStepTitle" className={style["slide-step-title"]}> 일정 등록 </span>
                            </div>
                        </div>
                    </SwiperSlide>
                    <SwiperSlide>
                        <div id="swiperSlide1" className={style["swiper-slide"]}>
                            <div id ="slideTitleBox" className={style["slide-title-box"]}>
                                <span id="slideStepTitle" className={style["slide-step-title"]}> 1단계 </span>
                                <span id="slideStepSubtitle" className={style["slide-step-subtitle"]}> 주제 선택</span>
                            </div>
                                <div id="slideBodyContainer" className ={style["slide-body-container"]}>
                                    <div className={style["slide-box-wrapper"]}>
                                        <div className={style["slide-body-top-box"]}>
                                            {targetBias.bid === "" ? (
                                                <div className={style["target-bias"]}></div>
                                            ) : (
                                                <img src={BIAS_URL + `${targetBias.bid}.png`} onError={(e) => (e.target.src = tempBias)}  />
                                            )}
                                            <span className={style["top-box-content"]}> 
                                                {targetBias.bname}
                                            </span>
                                        </div>
                                        <div className={style["slide-body-bottom-box"]}>
                                            {biasList.map((item, i) => {
                                                return <div onClick={() => handleSelectBias(i)} key={i} className={style["bias-box"]}>
                                                    <ScheduleTopic key={i} {...item} style={{width: "90%"}} />
                                                </div>
                                            })}
                                        </div>
                                    </div>
                                </div>
                                <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                    <div className={style["bottom-button"]}
                                        onClick={() => {
                                            navigate(-1);
                                        }}
                                    >
                                        취소
                                    </div>
                                    <div className={style["bottom-button"]}
                                        onClick={() => {
                                        if (targetBias.bid === "") {
                                            alert("선택된 주제가 없어요.");
                                        } else {
                                            swiperRef.current?.slideNext(); // 오른쪽 슬라이드 이동
                                            fetchSearchSchedule(); // 검색된 스케줄 가져오기
                                        }
                                    }}
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
                                            {targetBias.bid === "" ? (
                                                <div className={style["target-bias"]}></div>
                                            ) : (
                                                <img src={BIAS_URL + `${targetBias.bid}.png`} onError={(e) => (e.target.src = tempBias)}  />
                                            )}
                                            <span className={style["top-box-content"]}> 
                                                {targetBias.bname}
                                            </span>
                                        </div>
                                        <div className={style["slide-body-bottom-box"]}> 
                                            {searchedSchedule.length === 0 ? (
                                                <div className={style["no-content-message"]}>등록된 컨텐츠 일정이 없어요!</div>
                                            ) : (
                                                searchedSchedule.map((item, i) => (
                                                    <div>
                                                        <ScheduleCard key={i} {...item} style={{ width: "90%" }} />
                                                    </div>
                                                ))
                                            )}
                                        </div>
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
                                        <div className={style["input-slide-container"]}>
                                            <Swiper
                                                style={{width: "100%", height: "100%"}}
                                                onSwiper={(swiper) => (inputSwiperRef.current = swiper)} // Swiper 인스턴스 참조
                                                onSlideChange={handleMakeNewSchedule} // 슬라이드 변경 이벤트
                                            >
                                                {makeScheduleList.map(({id, index}, i) => (
                                                    <SwiperSlide key={id}>
                                                        <ScheduleMakeSlideComponent activeIndex={activeIndex} index={index}
                                                            schedule={tempScheduleData.schedules[i]}
                                                            setSendScheduleData={setTempScheduleData} 
                                                            sendScheduleData={tempScheduleData}
                                                        />
                                                    </SwiperSlide>
                                                ))}
                                            </Swiper>
                                        </div>
                                    </div>
                                </div>
                                <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                    <div className={style["bottom-button"]}
                                        onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                    >
                                        이전으로
                                    </div>
                                    <div className={style["bottom-button"]}
                                        onClick={() => {
                                            swiperRef.current?.slideNext()
                                            makeSendScheduleData()
                                        }} 
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
                                                총 {makedScheduleData.length}개의 일정을 작성했어요.
                                            </span>
                                        </div>
                                        <div className={style["slide-body-bottom-box"]}> 

                                            {makedScheduleData.map((item, i) => {
                                                return <div>
                                                    <ScheduleCard key={i} {...item} style={{width: "90%"}} />
                                                </div>
                                            })}

                                        </div>
                                    </div>
                                </div>
                                <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                    <div className={style["bottom-button"]}
                                        onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                    >
                                        이전으로
                                    </div>
                                    <div className={style["bottom-button"]}
                                        onClick={() => {
                                            swiperRef.current?.slideNext()
  
                                            tryFetchMakeSchedule()
                                        }} // 오른쪽 슬라이드 이동
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
                            <div style={{width: "100%", display: "flex", justifyContent: "center", alignItems: "center"}}>
                                <div className={style["bottom-button"]}
                                    onClick={() => {
                                        navigate("/schedule") // 오른쪽 슬라이드 이동
                                    }} // 오른쪽 슬라이드 이동
                                >
                                돌아가기
                                </div>
                            </div>
                        </div>
                    </SwiperSlide>
                </Swiper>
            </div>
        </div>
    );
  }else{
    return(
        <DesktopLayout>
            <div className="container">
                <div className={style["body-container"]} >
                    <Swiper 
                        style={{width: "100%", height: "100%"}}
                        direction={'vertical'}
                        onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
                        onSlideChange={handleSlideChange} // 슬라이드 변경 이벤트
                        speed={1000} // 슬라이드 전환 속도 1초
                        allowTouchMove={false}
                        touchEventsTarget="wrapper"
                    >
                        <SwiperSlide>
                            <div id="swiperSlide0" className={style["swiper-slide"]}>
                                <div id ="slideTitleBox" className={style["slide-title-box"]}>
                                    <span id="slideStepTitle" className={style["slide-step-title"]}> 일정 등록 </span>
                                </div>
                            </div>
                        </SwiperSlide>
                        <SwiperSlide>
                            <div id="swiperSlide1" className={style["swiper-slide"]}>
                                <div id ="slideTitleBox" className={style["slide-title-box"]}>
                                    <span id="slideStepTitle" className={style["slide-step-title"]}> 1단계 </span>
                                    <span id="slideStepSubtitle" className={style["slide-step-subtitle"]}> 주제 선택</span>
                                </div>
                                    <div id="slideBodyContainer" className ={style["slide-body-container"]}>
                                        <div className={style["slide-box-wrapper"]}>
                                            <div className={style["slide-body-top-box"]}>
                                                {targetBias.bid === "" ? (
                                                    <div className={style["target-bias"]}></div>
                                                ) : (
                                                    <img src={BIAS_URL + `${targetBias.bid}.png`} onError={(e) => (e.target.src = tempBias)}  />
                                                )}
                                                <span className={style["top-box-content"]}> 
                                                    {targetBias.bname}
                                                </span>
                                            </div>
                                            <div className={style["slide-body-bottom-box"]}>
                                                {biasList.map((item, i) => {
                                                    return <div onClick={() => handleSelectBias(i)} key={i} className={style["bias-box"]}>
                                                        <ScheduleTopic key={i} {...item} style={{width: "90%"}} />
                                                    </div>
                                                })}
                                            </div>
                                        </div>
                                    </div>
                                    <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                        <div className={style["bottom-button"]}
                                            onClick={() => {
                                                navigate(-1);
                                            }}
                                        >
                                            취소
                                        </div>
                                        <div className={style["bottom-button"]}
                                            onClick={() => {
                                            if (targetBias.bid === "") {
                                                alert("선택된 주제가 없어요.");
                                            } else {
                                                swiperRef.current?.slideNext(); // 오른쪽 슬라이드 이동
                                                fetchSearchSchedule(); // 검색된 스케줄 가져오기
                                            }
                                        }}
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
                                                {targetBias.bid === "" ? (
                                                    <div className={style["target-bias"]}></div>
                                                ) : (
                                                    <img src={BIAS_URL + `${targetBias.bid}.png`} onError={(e) => (e.target.src = tempBias)}  />
                                                )}
                                                <span className={style["top-box-content"]}> 
                                                    {targetBias.bname}
                                                </span>
                                            </div>
                                            <div className={style["slide-body-bottom-box"]}> 
                                                {searchedSchedule.length === 0 ? (
                                                    <div className={style["no-content-message"]}>등록된 컨텐츠 일정이 없어요!</div>
                                                ) : (
                                                    searchedSchedule.map((item, i) => (
                                                        <div>
                                                            <ScheduleCard key={i} {...item} style={{ width: "90%" }} />
                                                        </div>
                                                    ))
                                                )}
                                            </div>
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
                                            <div className={style["input-slide-container"]}>
                                                <Swiper
                                                    style={{width: "100%", height: "100%"}}
                                                    onSwiper={(swiper) => (inputSwiperRef.current = swiper)} // Swiper 인스턴스 참조
                                                    onSlideChange={handleMakeNewSchedule} // 슬라이드 변경 이벤트
                                                >
                                                    {makeScheduleList.map(({id, index}, i) => (
                                                        <SwiperSlide key={id}>
                                                            <ScheduleMakeSlideComponent activeIndex={activeIndex} index={index}
                                                                schedule={tempScheduleData.schedules[i]}
                                                                setSendScheduleData={setTempScheduleData} 
                                                                sendScheduleData={tempScheduleData}
                                                            />
                                                        </SwiperSlide>
                                                    ))}
                                                </Swiper>
                                            </div>
                                        </div>
                                    </div>
                                    <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                        <div className={style["bottom-button"]}
                                            onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                        >
                                            이전으로
                                        </div>
                                        <div className={style["bottom-button"]}
                                            onClick={() => {
                                                swiperRef.current?.slideNext()
                                                makeSendScheduleData()
                                            }} 
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
                                                    총 {makedScheduleData.length}개의 일정을 작성했어요.
                                                </span>
                                            </div>
                                            <div className={style["slide-body-bottom-box"]}> 

                                                {makedScheduleData.map((item, i) => {
                                                    return <div>
                                                        <ScheduleCard key={i} {...item} style={{width: "90%"}} />
                                                    </div>
                                                })}

                                            </div>
                                        </div>
                                    </div>
                                    <div id="slideBottomContainer" className={style["slide-bottom-container"]}>
                                        <div className={style["bottom-button"]}
                                            onClick={() => swiperRef.current?.slidePrev()} // 오른쪽 슬라이드 이동
                                        >
                                            이전으로
                                        </div>
                                        <div className={style["bottom-button"]}
                                            onClick={() => {
                                                swiperRef.current?.slideNext()
  
                                                tryFetchMakeSchedule()
                                            }} // 오른쪽 슬라이드 이동
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
                                <div style={{width: "100%", display: "flex", justifyContent: "center", alignItems: "center"}}>
                                    <div className={style["bottom-button"]}
                                        onClick={() => {
                                            navigate("/schedule") // 오른쪽 슬라이드 이동
                                        }} // 오른쪽 슬라이드 이동
                                    >
                                    돌아가기
                                    </div>
                                </div>
                            </div>
                        </SwiperSlide>
                    </Swiper>
                </div>
            </div>
        </DesktopLayout>
    );
  }
};

export default ScheduleMakePage;