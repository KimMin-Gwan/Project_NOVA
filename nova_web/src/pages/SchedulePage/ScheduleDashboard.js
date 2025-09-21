import "./style.css";
import { useNavigate } from "react-router-dom";
import React, { useRef, useEffect, useState } from "react";
//import TimeChart from "./TimeChart/TimeChart.jsx";
import Header from "../../component/Header/Header.js";
import HEADER from "../../constant/header";
import postApi from "../../services/apis/postApi.js";
import mainApi from "../../services/apis/mainApi.js";
import NavBar from "../../component/NavBar/NavBar.js";
import TimeLayerBox from "./time_layer/time_layer_box.js";

import { Swiper, SwiperSlide } from "swiper/react";

import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

import style from './../FeedDetail/NewFeedDetail.module.css';
import style2 from './time_layer/TimeLayerBoxDesktop.module.css';

import arrowRightStop from './Arrow_right_stop.svg';
import tempBias from "./../../img/tempBias.png";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout.jsx";
import TimeLayerBoxDesktop from "./time_layer/time_layer_box_desktop.jsx";
import ScheduleDetailDekstop from "../../component/ScheduleDetail/ScheduleDetailDesktop.jsx";
import ScheduleDetailMobile from "../../component/ScheduleDetail/ScheduleDetailMobile.jsx";


const temp_schedule_data2 = [
    { tag : "노래/음악"},
    { section : "새벽", schedules : [
        ]
    },
    { section : "오전", schedules : [
        { time: "AM 11:00", type: "추천", schedule_id: "aaa", schedule_title: "아침 노래뱅", schedule_bias: "주제이름1" },
        { time: "AM 11:00", type: "구독", schedule_id: "bbb", schedule_title: "한식 맛집 아테의 노래뱅", schedule_bias: "주제이름2" },
        ]
    },
    { section : "오후", schedules : [
        { time: "PM 01:00", type: "추천", schedule_id: "ccc", schedule_title: "마지막 노래 방송", schedule_bias: "주제이름2" },
        ]
    },
    { section : "저녁", schedules : [
        { time: "PM 07:00", type: "구독", schedule_id: "3", schedule_title: "잔잔노래짧뱅", schedule_bias: "주제이름4" },
        { time: "PM 08:00", type: "추천", schedule_id: "4", schedule_title: "이쁜이들이랑 싱크룸", schedule_bias: "주제이름5" },
        ]
    }
    //{ section : "오전", schedules : [
        //{ time: "AM 11:00", type: "recommened", schedule_id: "0", schedule_title: "아침 노래뱅", schedule_bias: "성화린" },
        //{ time: "AM 11:00", type: "recommened", schedule_id: "1", schedule_title: "한식 맛집 아테의 노래뱅", schedule_bias: "김아테" },
        //]
    //},
    //{ section : "오후", schedules : [
        //{ time: "PM 01:00", type: "added", schedule_id: "2", schedule_title: "마지막 노래 방송", schedule_bias: "슈메히메" },
        //]
    //},
    //{ section : "저녁", schedules : [
        //{ time: "PM 07:00", type: "recommened", schedule_id: "3", schedule_title: "잔잔노래짧뱅", schedule_bias: "후츄후츄" },
        //{ time: "PM 08:00", type: "recommened", schedule_id: "4", schedule_title: "이쁜이들이랑 싱크룸", schedule_bias: "밍수진" },
        //]
    //}
]

const temp_schedule_data = [
    { tag : ""},
    { section : "새벽", schedules : [ ] },
    { section : "오전", schedules : [ ] },
    { section : "오후", schedules : [ ] },
    { section : "저녁", schedules : [ ] }
]

const ScheduleDashboard = () => {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const navigate = useNavigate();

  const [makeScheduleModal, setMakeScheduleModal] = useState(false);

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleMakeScheduleModal = (target) => {
    setMakeScheduleModal((makeScheduleModal) => !makeScheduleModal);
  };

  //let [weekDayData, setWeekDayData] = useState([]);
  let [scheduleData, setScheduleData] = useState([temp_schedule_data]);
  //let [eventData, setEventData] = useState([]);

  let [targetMonth, setTargetMonth] = useState("00년 00월");
  let [targetWeek, setTargetWeek] = useState("0주차");
  let [numBias, setNumBias] = useState(0);
  let [numSchedule, setNumSchedule] = useState(0);

  let [biasData, setBiasData] = useState([]);

  //const [pageIndex, setPageIndex] = useState(0);
  const [targetDate, setTargetDate] = useState(new Date());
  const [leftTargetDate, setLeftTargetDate] = useState(targetDate);
  const [rightTargetDate, setRightTargetDate] = useState(targetDate);

  // 4. 26. 토요일 이렇게 나오게 하려고 만든거
  const getFormattedDate = (date) => {
    const formatter = new Intl.DateTimeFormat('ko-KR', {
      month: 'numeric',    // 4
      day: 'numeric',      // 26
      weekday: 'long',     // 토요일
    });

    return formatter.format(date)
  }

  const [showScheduleMoreOption, setShowScheduleMoreOption] = useState(false);
  const [targetSchedule, setTargetSchedule] = useState("");

  const toggleMoreOption = (targetSchedule) => {
    setTargetSchedule(targetSchedule);
    setShowScheduleMoreOption(!showScheduleMoreOption);
  }

  const [formatDate, setFormatDate] = useState([getFormattedDate(targetDate)])


  async function justFetchPrevData() {
    // 일단 왼쪽 날짜를 하나 지워야됨
    const yieldDate = new Date(leftTargetDate); // 기존 날짜 복사
    yieldDate.setDate(leftTargetDate.getDate() - 1); // 날짜를 계산
    setLeftTargetDate(yieldDate);

    const dateString = yieldDate.toISOString().split("T")[0].replace(/-/g, "/");

    const newSchedule = await fetchScheduleDataWithDate(dateString)
    setScheduleData((prev) => [newSchedule, ...prev])
    setFormatDate((prev) => [getFormattedDate(yieldDate), ...prev])
  }

  async function onChangeIndexPrev() {
    const activeIndex = swiperRef2.current?.activeIndex
    // 일단 왼쪽 날짜를 하나 지워야됨
    const yieldDate = new Date(leftTargetDate); // 기존 날짜 복사
    yieldDate.setDate(leftTargetDate.getDate() - 1); // 날짜를 계산
    setLeftTargetDate(yieldDate);

    const dateString = yieldDate.toISOString().split("T")[0].replace(/-/g, "/");

    const newSchedule = await fetchScheduleDataWithDate(dateString)
    setScheduleData((prev) => [newSchedule, ...prev])
    setFormatDate((prev) => [getFormattedDate(yieldDate), ...prev])

    setTimeout(() => {
        if (swiperRef2.current) {
            // 1. 현재 활성화된 슬라이드 위치 유지
            swiperRef2.current.slideTo(activeIndex + 1, 0); 
            
            // 2. 새 슬라이드로 이동
            setTimeout(() => {
                swiperRef2.current.slideTo(0, 300); // 새 슬라이드로 300ms 동안 이동
            }, 100); // 상태 변경 반영 후 동작하도록 약간의 지연 추가
        }
    }, 0);
  }


  async function onChangeNextAsync(){
    const activeIndex = swiperRef2.current?.activeIndex

    await onChangeIndexNext()
    setTimeout(() => {
        if (swiperRef2.current) {
            // 1. 현재 활성화된 슬라이드 위치 유지
            swiperRef2.current.slideTo(activeIndex + 1, 0); 
            
            // 2. 새 슬라이드로 이동
            setTimeout(() => {
                swiperRef2.current?.slideNext()
                //swiperRef2.current.slideTo(0, 300); // 새 슬라이드로 300ms 동안 이동
            }, 100); // 상태 변경 반영 후 동작하도록 약간의 지연 추가
        }
    }, 0);
  }


  async function onChangeIndexNext() {
    const yieldDate = new Date(rightTargetDate);
    yieldDate.setDate(rightTargetDate.getDate() + 1);
    setRightTargetDate(yieldDate);

    const dateString = yieldDate.toISOString().split("T")[0].replace(/-/g, "/");
    const newSchedule = await fetchScheduleDataWithDate(dateString);

    setScheduleData((prev) => {
      const updated = [...prev, newSchedule];
      return updated;
    });

    setFormatDate((prev) => [...prev, getFormattedDate(yieldDate)]);
  }


  const brightMode = "brigthMode";

  // 네비게이션 함수
  const handleNavigate = (path) => {
    navigate(`${path}`);
  };

  // 주간 날짜 받기
  function fetchTargetMonthWeek(date) {
    mainApi.get(`time_table_server/try_get_dashboard_data?date=${date}`).then((res) => {
      setTargetMonth(res.data.body.target_month);
      setTargetWeek(res.data.body.target_week);
      setNumBias(res.data.body.num_bias);
      setNumSchedule(res.data.body.num_schedules);
    });
  }


  //// 시간 차트 데이터 받기
  //function fetchTimeChartData(date) {
    //mainApi.get(`time_table_server/try_get_today_time_chart?date=${date}`).then((res) => {
      //setScheduleData(res.data.body.schedule_blocks);
      //setWeekDayData(res.data.body.week_day_datas);
    //});
  //}

  // 시간 레이어 데이터 받기
  async function fetchScheduleDataWithDate(date) {
    try {
      const res = await mainApi.get(`/time_table_server/get_time_layer_schedule_with_date?date=${date}`);
      return res.data.body.schedule_layer; // 반환값을 명시적으로 설정
    } catch (error) {
      return temp_schedule_data
    }
  }

  //// 시간 레이어 데이터 받기
  //async function fetchScheduleDataWithDate(date) {
    //return temp_schedule_data2
  //}


  //useEffect(() => {
    //const dateString = targetDate.toISOString().split("T")[0]; // 'YYYY-MM-DD' 형식으로 변환
    //fetchTargetMonthWeek(dateString);
    ////fetchTimeChartData(dateString);
    ////fetchScheduleDataWithDate(dateString);
  //}, [targetDate]);

  async function initDataSetting(dateString){
    const newSchedule = await fetchScheduleDataWithDate(dateString)
    setScheduleData([newSchedule])
    return
  }

  useEffect(() => {
    const dateString = targetDate.toISOString().split("T")[0].replace(/-/g, "/");
    fetchTargetMonthWeek(dateString);
    initDataSetting(dateString)
  }, []);


  // ------------------------------------- 스와이퍼 부분 -------------------------------------

  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성
  const swiperRef2 = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성

  const [rightRotation, setRightRotation] = useState(180);
  const [leftRotation, setLeftRotation] = useState(0);

  function calculateRightRotation(diff) {
    const inputMin = -300;
    const inputMax = -100;
    const outputMin = 0;
    const outputMax = 180;

    // 선형 변환 공식
    const rotation = ((diff - inputMin) / (inputMax - inputMin)) * (outputMax - outputMin) + outputMin;
    //console.log(diff)

    // 변환된 값을 상태로 설정
    setRightRotation(rotation);

  }
  function calculateLeftRotation(diff) {
    const inputMin = 300;
    const inputMax = 100;
    const outputMin = 180;
    const outputMax = 0;

    // 선형 변환 공식
    const rotation = ((diff - inputMin) / (inputMax - inputMin)) * (outputMax - outputMin) + outputMin;
    // 변환된 값을 상태로 설정
    setLeftRotation(rotation);

  } 

  const [editScheduleModal, setEditScheduleModal] = useState(false);
  const [editTarget, setEditTarget] = useState({sid:""})

  const toggleEditScheduleModal = (target) => {
    setEditScheduleModal((editScheduleModal) => !editScheduleModal);
    setEditTarget({sid:target})
  };

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFetching, setIsFetching] = useState(false);
  const [lastAction, setLastAction] = useState(null);

  const handleNext = async () => {
    if (isFetching) return;
    setIsFetching(true);
    await onChangeIndexNext();
    setLastAction('next');
    setIsFetching(false);
  };

  const handlePrev = async () => {
    if (isFetching) return;
    setIsFetching(true);
    await justFetchPrevData();
    setLastAction('prev');
    setIsFetching(false);
  };

  useEffect(() => {
    if (!isFetching && scheduleData.length > 0) {
      if (lastAction === 'next') {
        setCurrentIndex((prev) => (prev + 1) % scheduleData.length);
      } else if (lastAction === 'prev') {
        // prev는 index 유지하거나 필요시 조정
        setCurrentIndex((prev) => prev); 
      }
    }
  }, [scheduleData, lastAction]);


  if(isMobile){
    return (
      <div className="container">
        <div className="body-box">
          <Header />

          <div className="section-box">
            <div className="dashboard-section">
              <div className="section-title">
                <p className="element">
                  <span className="text-wrapper">{targetMonth} </span>
                  <span className="span">{targetWeek}</span>
                </p>
              </div>
              <div className="my-dashboard">
                <div className="left-group">
                  <span>이번주 컨텐츠</span>
                  <span className="num-bias">{numSchedule}</span>
                  <span>개</span>
                </div>
                <div className="right-group">
                  {/* <button onClick={() => handleNavigate("/schedule/my_schedule")}>내 일정</button> 
                  <img src={vertical_line} alt="vertical line" />*/}

                  <button onClick={() => {
                    mainApi.get("home/is_valid").then((res) => {
                      navigate("/schedule/make_new")
                    })
                    .catch((err) => {
                      if (err.response.status === 401) {
                        navigate("/novalogin")
                      }else{
                      }
                    })
                  }}>일정 등록</button>
                </div>
              </div>
            </div>
          </div>

          <div className="section-separator"></div>

          <div className="section-box">
            <div className="dashboard-section" style={{paddingBottom: "0px"}}>
              <div className="section-title">
                <p className="element">
                  <span className="text-wrapper">컨텐츠 목록</span>
                </p>
                <span className="add-schedule" onClick={() => handleNavigate("/explore/schedule")}>
                  일정 탐색
                </span>
              </div>
            </div>

            {/**   타임차트 만들던 곳
            <TimeChart
              weekDayData={weekDayData}
              scheduleData={scheduleData}
              onChangeIndex={onChangeIndex}
            />
            */}
            <div style={{display: "flex", justifyContent:"center", alignContent:"center"}}>
              {showScheduleMoreOption && (
                <ScheduleDetailMobile
                  sid={targetSchedule}
                  toggleMoreOption={toggleMoreOption}
                />
              )}

              <Swiper
                initialSlide={1}
                centeredSlides={true} // 중앙 정렬
                //loop={true} // 무한 루프
                onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
                onSlideChange={(swiper) => {
                  if (swiper.activeIndex === 0) {
                    // 0번 슬라이드로 이동하면 강제로 1번 슬라이드로 이동
                    setTimeout(() => swiperRef.current?.slideTo(1), 0);
                    // 당기면 지난주 데이터를 받아야하는데, 너무 민감해서 diff 차이로 계산
                    if (swiper.touches.diff > 200){
                      onChangeIndexPrev();
                    }
                  }
                  else if (swiper.activeIndex === 2){
                    // 5번 슬라이드로 이동하면 강제로 4번 슬라이드로 이동
                    setTimeout(() => swiperRef.current?.slideTo(1), 0);
                    // 당기면 다음주 데이터를 받아야하는데, 너무 민감해서 diff 차이로 계산
                    if (swiper.touches.diff < -200){
                      onChangeNextAsync()
                    }
                  }else{
                  }
                }}
                onTransitionStart={(swiper) => {
                  // 화살표 돌리기 로직 (초기화 로직)
                    if (swiper.activeIndex == 1)
                    {
                      setLeftRotation(0);
                      setRightRotation(180);
                    }
            
                    //else if (swiper.activeIndex == 1){
                      //setRightRotation(180);
                    //}
                }}
                onTouchMove={(swiper) => {
                  // 화살표 돌리기 로직
                  //if (swiper.activeIndex== 4){
                  if (swiper.activeIndex== 1){
                    if (swiper.touches.diff < -99 && swiper.touches.diff > -301){
                      if (parseInt(swiper.touches.diff) % -10 == 0){
                        calculateRightRotation(swiper.touches.diff);
                      }
                    }
                  }
                  if (swiper.activeIndex== 1){
                    if (swiper.touches.diff > 99 && swiper.touches.diff < 301){
                      if (parseInt(swiper.touches.diff) % 10 == 0){
                        calculateLeftRotation(swiper.touches.diff);
                      }
                    }
                  }
                }}
                //allowSlidePrev={allowPrev} // 이전 슬라이드 이동 허용 여부
              >
                <SwiperSlide key={0}>
                  <div className="load-week-container-new"
                    style={{justifyContent:'flex-end'}}
                  >
                      <span className="load-text">지난 날 불러오기</span>
                      <div>
                        <img
                          src={arrowRightStop}
                          className="arrow-img"
                          style={{ transform: `rotate(${leftRotation}deg)` }}
                        />
                      </div>
                  </div>
                </SwiperSlide>
                <SwiperSlide>
                <Swiper
                  onSwiper={(swiper) => (swiperRef2.current = swiper)} // Swiper 인스턴스 참조
                >
                {
                  scheduleData.length === 0 ? (
                    <div className="loading-screen">
                      로딩 중...
                    </div>
                  ) : (
                    scheduleData.map((schedule, index) => {
                      return (
                        <SwiperSlide key={index}>
                          <TimeLayerBox swiperRef={swiperRef2} scheduleData={schedule} formattedDate={formatDate[index]} 
                          onChangeIndexNext={onChangeNextAsync} onChangeIndexPrev={onChangeIndexPrev}
                          scheduleDayList={scheduleData} onClickSchedule={toggleMoreOption}
                          />
                        </SwiperSlide>
                      );
                    })
                  )
                }
                </Swiper>


                </SwiperSlide>
                <SwiperSlide key={2}>
                  <div className="load-week-container-new"
                    style={{justifyContent:'flex-start'}}
                  >
                      <span className="load-text">다음 날 불러오기</span>
                      <div>
                        <img
                          src={arrowRightStop}
                          className="arrow-img"
                          style={{ transform: `rotate(${rightRotation}deg)` }}
                        />
                      </div>
                  </div>
                </SwiperSlide>
              </Swiper>
            </div>
          </div>

          <div className="section-separator"></div>

          <div className="section-box">
            <div className="dashboard-section">
              <div className="section-title">
                <p className="element">
                  <span className="text-wrapper">최근 콘텐츠 이슈</span>
                </p>
              </div>
            </div>
            <div className={style["content-issue-box"]}>
              준비중입니다.
            </div>
          </div>
        </div>

        <NavBar brightMode={brightMode} />
      </div>
    );
  }else{
    return(
    <DesktopLayout>
        <div className={style2["schedule-dashboard-main-frame"]}>
          {showScheduleMoreOption && (
            <ScheduleDetailDekstop
              sid={targetSchedule}
              toggleMoreOption={toggleMoreOption}
            />
          )}
          {
            scheduleData.length === 0 ? (
              <div className="loading-screen">
                로딩 중...
              </div>
            ) : (
              <TimeLayerBoxDesktop
                scheduleData={scheduleData[currentIndex]}
                formattedDate={formatDate[currentIndex]}
                onChangeIndexNext={handleNext}
                onChangeIndexPrev={handlePrev}
                isFetching={isFetching}
                onClickSchedule={toggleMoreOption}
              />
            )
          }
        </div>
    </DesktopLayout>
    );
  }

};



export default ScheduleDashboard;

//  // 오늘짜 이벤트 데이터 받아오고
//// 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
//function fetchEventData() {
//mainApi.get("time_table_server/try_get_event_board_data").then((res) => {
//setEventData(res.data.body.schedule_events);
//});
//}
// 댓글 옵션 모달
