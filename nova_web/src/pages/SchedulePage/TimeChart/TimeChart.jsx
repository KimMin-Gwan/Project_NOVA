import React, { useRef, useState, useEffect } from "react";
import "./time_chart_style.css"; // 스타일 파일
import ChartScheduleComponent from "../ChartScheduleComponent"; // 일정 컴포넌트
import arrow_drop_left from "./../../../img/Arrow_drop_left.svg"; // 왼쪽 화살표 이미지
import arrow_drop_right from "./../../../img/Arrow_drop_right.svg"; // 오른쪽 화살표 이미지
import TimeWeekComponent from "./TImeWeekComponent"; // 주간 요일 컴포넌트
import arrowRightStop from './Arrow_right_stop.svg';

// Swiper 관련 모듈
import { Autoplay, Pagination } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";

import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

// 시간 리스트와 시간 섹션 정의
//const timeList = [
  //["00:00", "01:00", "02:00", "03:00", "04:00", "05:00"],
  //["06:00", "07:00", "08:00", "09:00", "10:00", "11:00"],
  //["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
  //["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
//];
const timeList = [
  ["00시", "01시", "02시", "03시", "04시", "05시"],
  ["06시", "07시", "08시", "09시", "10시", "11시"],
  ["12시", "13시", "14시", "15시", "16시", "17시"],
  ["18시", "19시", "20시", "21시", "22시", "23시"],
];

const timeSectionList = ["새벽", "오전", "오후", "밤"]; // 시간 섹션 이름

export default function TimeChart({ weekDayData, scheduleData }) {
  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성

  const findSection = () => {
    const currentHour = new Date().getHours(); // 현재 시간의 '시'를 가져옴

    // 시간대 인덱스 계산
    if (currentHour >= 0 && currentHour < 6) {
      return 1
    } else if (currentHour >= 6 && currentHour < 12) {
      return 2
    } else if (currentHour >= 12 && currentHour < 18) {
      return 3
    } else if (currentHour >= 18 && currentHour < 24) {
      return 4
    }
  }

  const handleSlideChange = (swiper) => {
    if (swiper.activeIndex === 1) {
      return false; // 첫 번째 슬라이드에서는 이전 슬라이드 이동 막음
    }
    else{
      return true;
    }
  }

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

    // 완전히 당기면 새로고침 하는 코드 여기
    //if (rotation == 0){
      //fetchData()
    //}
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

    // 완전히 당기면 새로고침 하는 코드 여기
    //if (rotation == 180){
      //fetchData()
    //}
  }

  const [rotateImage, setRotateImage] = useState(false);

  return (
    <div className="time-chart-box">
      {/* 요일 및 기타 정보 표시 */}
      <div className="day-week-list">
        <div className="chart-etc-box"></div> {/* 기타 구성 요소 */}
        <div>
          {/* 요일 데이터를 렌더링 */}
          {weekDayData.map((item, i) => (
            <TimeWeekComponent key={i} {...item} />
          ))}
        </div>
      </div>

      {/* Swiper 컴포넌트 */}
      <Swiper
        centeredSlides={true} // 중앙 정렬
        //loop={true} // 무한 루프
        onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
        initialSlide={findSection()}
        onSlideChange={(swiper) => {
          if (swiper.activeIndex === 0) {
            // 0번 슬라이드로 이동하면 강제로 1번 슬라이드로 이동
            setTimeout(() => swiperRef.current?.slideTo(1), 0);
          }
          else if (swiper.activeIndex === 5){
            setTimeout(() => swiperRef.current?.slideTo(4), 0);
          }
        }}
        onTransitionStart={(swiper) => {
            if (swiper.activeIndex == 1)
            {
              setLeftRotation(0);
            }else if (swiper.activeIndex == 4){
              setRightRotation(180);
            }
        }}
        onTouchMove={(swiper) => {
          if (swiper.activeIndex== 4){
            if (swiper.touches.diff < -99 && swiper.touches.diff > -301){
              if (swiper.touches.diff % -10 == 0){
                calculateRightRotation(swiper.touches.diff);
              }
            }
          }
          if (swiper.activeIndex== 1){
            if (swiper.touches.diff > 99 && swiper.touches.diff < 301){
              if (swiper.touches.diff % 10 == 0){
                calculateLeftRotation(swiper.touches.diff);
              }
            }
          }
        }}
        //allowSlidePrev={allowPrev} // 이전 슬라이드 이동 허용 여부
      >
        <SwiperSlide key={0}>
          <div className="load-week-container"
            style={{justifyContent:'flex-end'}}
          >
              <span className="load-text">지난 주 불러오기</span>
              <div>
                <img
                  src={arrowRightStop}
                  className="arrow-img"
                  style={{ transform: `rotate(${leftRotation}deg)` }}
                />
              </div>
          </div>
        </SwiperSlide>
        {timeSectionList.map((item, j) => (
          <SwiperSlide key={j+1}>
            <div className="chart-box">
              {/* 시간 선택 및 화살표 */}
              <div className="time-select-box">
                <img
                  src={arrow_drop_left}
                  alt="arrow left"
                  onClick={() => swiperRef.current?.slidePrev()} // 왼쪽 슬라이드 이동
                  style={{ cursor: "pointer" }} // 클릭 가능 표시
                />
                <span>{item} 타임</span>
                <img
                  src={arrow_drop_right}
                  alt="arrow right"
                  onClick={() => swiperRef.current?.slideNext()} // 오른쪽 슬라이드 이동
                  style={{ cursor: "pointer" }} // 클릭 가능 표시
                />
              </div>

              {/* 시간 라인 표시 */}
              <div className="time-line-box">
                {timeList[j].map((time, i) => (
                  <span key={i}>{time}</span> // 각 시간 표시
                ))}
              </div>

              {/* 스케줄 데이터 렌더링 */}
              <div className="schedule-box-list">
                {scheduleData.map((item, i) => (
                  <ChartScheduleComponent key={i} {...item} timeSection={j} />
                ))}
              </div>
            </div>
          </SwiperSlide>
        ))}
        <SwiperSlide key={5}>
          <div className="load-week-container"
            style={{justifyContent:'flex-start'}}
          >
              <span className="load-text">다음 주 불러오기</span>
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
  );
}


export function TimeChartPreview({ weekDayData, scheduleData }) {
  const swiperRef = useRef(null); // Swiper 인스턴스를 참조하기 위한 Ref 생성

  console.log(scheduleData)

  // 초기화
  const findSection = () => {
    let maxTimeIndex = 3;

    if (scheduleData.length > 0){
      //console.log(scheduleData)
      //console.log(scheduleData[0].timeblocks)
      // scheduleData 반복 처리
      scheduleData.forEach(singleSchedule => {
        if(singleSchedule.timeblocks.length > 0){
          singleSchedule.timeblocks.forEach(block => {
            if (maxTimeIndex > block.time) {
              maxTimeIndex = block.time;
            }
          });
        }
      });
    }
    return maxTimeIndex
  }


  return (
    <div className="time-chart-box">
      {/* 요일 및 기타 정보 표시 */}
      <div className="day-week-list">
        <div className="chart-etc-box"></div> {/* 기타 구성 요소 */}
        <div>
          {/* 요일 데이터를 렌더링 */}
          {weekDayData.map((item, i) => (
            <TimeWeekComponent key={i} {...item} />
          ))}
        </div>
      </div>

      {/* Swiper 컴포넌트 */}
      <Swiper
        centeredSlides={true} // 중앙 정렬
        //loop={true} // 무한 루프
        onSwiper={(swiper) => (swiperRef.current = swiper)} // Swiper 인스턴스 참조
        initialSlide={findSection()}
        //onSlideChange={(swiper) => {
          //if (swiper.activeIndex === 0) {
            //// 0번 슬라이드로 이동하면 강제로 1번 슬라이드로 이동
            //setTimeout(() => swiperRef.current?.slideTo(1), 0);
          //}
          //else if (swiper.activeIndex === 5){
            //setTimeout(() => swiperRef.current?.slideTo(4), 0);
          //}
        //}}
        allowSlidePrev={(swiper)=>{if(swiper.activeIndex === 1){return false}else{return true}}} // 이전 슬라이드 이동 허용 여부
        allowSlideNext={(swiper)=>{if(swiper.activeIndex === 4){return false}else{return true}}} // 이전 슬라이드 이동 허용 여부
      >
        <SwiperSlide key={0}>
          <div className="load-week-container"
            style={{justifyContent:'flex-end'}}
          >
              <span className="load-text">여긴 없어요!</span>
          </div>
        </SwiperSlide>
        {timeSectionList.map((item, j) => (
          <SwiperSlide key={j+1}>
            <div className="chart-box">
              {/* 시간 선택 및 화살표 */}
              <div className="time-select-box">
                <img
                  src={arrow_drop_left}
                  alt="arrow left"
                  onClick={() => swiperRef.current?.slidePrev()} // 왼쪽 슬라이드 이동
                  style={{ cursor: "pointer" }} // 클릭 가능 표시
                />
                <span>{item} 타임</span>
                <img
                  src={arrow_drop_right}
                  alt="arrow right"
                  onClick={() => swiperRef.current?.slideNext()} // 오른쪽 슬라이드 이동
                  style={{ cursor: "pointer" }} // 클릭 가능 표시
                />
              </div>

              {/* 시간 라인 표시 */}
              <div className="time-line-box">
                {timeList[j].map((time, i) => (
                  <span key={i}>{time}</span> // 각 시간 표시
                ))}
              </div>

              {/* 스케줄 데이터 렌더링 */}
              <div className="schedule-box-list">
                {scheduleData.map((item, i) => (
                  <ChartScheduleComponent key={i} {...item} timeSection={j} />
                ))}
              </div>
            </div>
          </SwiperSlide>
        ))}
        <SwiperSlide key={5}>
          <div className="load-week-container"
            style={{justifyContent:'flex-start'}}
          >
              <span className="load-text">여기도 없어요!</span>
          </div>
        </SwiperSlide>
      </Swiper>
    </div>
  );
}