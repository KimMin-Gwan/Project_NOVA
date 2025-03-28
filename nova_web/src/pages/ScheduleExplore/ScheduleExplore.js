import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Swiper, SwiperSlide } from "swiper/react";
import { Scrollbar } from "swiper/modules";
import "swiper/css";
import "swiper/css/scrollbar";
import back from "./../../img/detail_back.png";
import arrow from "./../../img/explore_down.png";
import useToggleMore from "../../hooks/useToggleMore";

import "./index.css";

export default function ScheduleExplore() {
  const { moreClick, handleToggleMore } = useToggleMore();
  const navigate = useNavigate();

  const [modalButton, setModalButton] = useState(false);

  const scheduleKind = ["게임", "저챗", "음악", "그림", "스포츠", "시참"];
  const swiperRef = useRef(null);
  const [activeIndex, setActiveIndex] = useState(0);

  const [buttonType, setButtonType] = useState("");
  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  // 누르면 키가 자꾸 올라가는 문제가 있음 !!!!
  const handleClick = (index) => {
    setActiveIndex(index);
    swiperRef.current.swiper.slideTo(index);
  };

  useEffect(() => {
    console.log(activeIndex);
  }, [activeIndex]);

  function handleModal(type) {
    setModalButton((modalButton) => !modalButton);
    setButtonType(type);
  }

  // 슬라이드 변경 시 활성화된 탭을 동기화
  const handleTabChange = (swiper) => {
    setActiveIndex(swiper.activeIndex);
  };

  return (
    <div className="container ExploreSchedulePage">
      <nav className="navBar">
        <button>
          <img src={back} alt="" />
          뒤로
        </button>
        <h1>일정 탐색</h1>
        <p>3월 4째주</p>
      </nav>
      <section className={"type-list"}>
        <ul className={"post-list"} data-active-index={activeIndex}>
          <TabItem
            tabs={scheduleKind}
            activeIndex={activeIndex}
            handleClick={handleClick}
          />
        </ul>
      </section>
      {/* 화면이 530px 이하일 때 슬라이더로 탭 대체 */}
      <section className="swiper-type">
        <Swiper
          spaceBetween={10}
          slidesPerView={4} // 여러 개의 탭을 동시에 보여주기
          onSlideChange={handleTabChange}
          ref={swiperRef}
          modules={[Scrollbar]}
          scrollbar={{ draggable: true }}
        >
          {scheduleKind.map((item, index) => (
            <SwiperSlide key={index}>
              <button
                className={activeIndex === index ? "active" : ""}
                onClick={() => handleClick(index)}
              >
                {item}
              </button>
            </SwiperSlide>
          ))}
        </Swiper>
      </section>

      <section className="button-container">
        <button onClick={() => handleModal("time")}>
          시간 설정 <img src={arrow} alt="" />
        </button>
        <button onClick={() => handleModal("style")}>
          방송 스타일 <img src={arrow} alt="" />
        </button>
        <button>
          성별 <img src={arrow} alt="" />
        </button>
      </section>
      <Swiper
        spaceBetween={50}
        slidesPerView={1}
        onSlideChange={handleTabChange}
        ref={swiperRef}
        className="scheduleList"
      >
        <ul>
          <SwiperSlide>
            <li>슬라이드 A</li>
          </SwiperSlide>
          <SwiperSlide>
            <li>슬라이드 B</li>
          </SwiperSlide>
          <SwiperSlide>
            <li>슬라이드 C</li>
          </SwiperSlide>
          <SwiperSlide>
            <li>슬라이드 D</li>
          </SwiperSlide>
          <SwiperSlide>
            <li>슬라이드 E</li>
          </SwiperSlide>
          <SwiperSlide>
            <li>슬라이드 F</li>
          </SwiperSlide>
        </ul>
      </Swiper>
      <ButtonModal
        closeSchedule={handleModal}
        isOpen={modalButton}
        type={buttonType}
      />
    </div>
  );
}

// Tabs 컴포넌트가 존재, 그거랑 합치기 필요
function TabItem({ tabs, activeIndex, handleClick }) {
  return (
    <>
      {tabs.map((tab, index) => (
        <li
          key={index}
          className={`post ${activeIndex === index ? "active" : ""}`}
          onClick={() => handleClick(index, tab)}
        >
          <button>{tab}</button>
        </li>
      ))}
    </>
  );
}

export function ButtonModal({ closeSchedule, isOpen, type }) {
  const [backgroundColor, setBackgroundColor] = useState("");
  const [displaySt, setdisplaySt] = useState("");
  const [upAnimation, setUpAnimation] = useState(false);

  const [selected, setSelected] = useState([]);

  const timeOptions = [
    { label: "새벽 일정", time: "00시 ~ 06시" },
    { label: "오전 일정", time: "06시 ~ 12시" },
    { label: "오후 일정", time: "12시 ~ 16시" },
    { label: "저녁 일정", time: "16시 ~ 24시" },
  ];

  const broadcastOptions = [
    { label: "캠 방송", value: "캠 방송" },
    { label: "노캠 방송", value: "노캠 방송" },
    { label: "버츄얼 방송", value: "버츄얼 방송" },
  ];

  const handleSelect = (value) => {
    if (value === "all") {
      setSelected(
        selected.length === 4
          ? []
          : ["새벽 일정", "오전 일정", "오후 일정", "저녁 일정"]
      );
    } else {
      setSelected((prev) =>
        prev.includes(value)
          ? prev.filter((item) => item !== value)
          : [...prev, value]
      );
    }
  };

  // 애니메이션 올라오면 배경색 변화도록 해주는 이펙트
  useEffect(() => {
    if (!isOpen) {
      setBackgroundColor("transparent"); //닫혀있을 때는 배경색 없애기
      setUpAnimation(false); // see 클래스 없애주기 위해서 닫히면 false 되도록 바꿔줌
      // 5초 뒤에 닫기도록
      setTimeout(() => {
        setdisplaySt("none");
      }, 500);
    } else {
      setdisplaySt("block");

      // 열렸다는 block 후에 애니메이션 적용 되도록 함
      setTimeout(() => {
        setUpAnimation(true);
      }, 10);

      //애니메이션 다하고 뒤에 배경색 주기
      setTimeout(() => {
        setBackgroundColor("rgba(0, 0, 0, 0.5)");
      }, 500);
    }

    return () => {
      clearTimeout();
    };
  }, [isOpen]);

  const renderCheckboxes = (options) => {
    return options.map((option) => (
      <label key={option.label}>
        <span>
          <p>{option.label}</p>
          {option.time && <p>{option.time}</p>}
        </span>
        <input
          type="checkbox"
          name="time"
          value={option.label}
          checked={selected.includes(option.label)}
          onChange={() => handleSelect(option.label)}
        />
      </label>
    ));
  };

  return (
    <div
      className={`EventMoreContainer ${upAnimation ? "see" : ""}`}
      onClick={closeSchedule}
      style={{ display: displaySt, backgroundColor }}
    >
      <section
        className={`eventMain ${isOpen ? "on" : ""}`}
        onClick={(e) => e.stopPropagation()}
      >
        {type === "time" ? (
          <>
            <h3>시간 설정</h3>
            <form className="form-container">
              <label>
                전체 선택
                <input
                  type="checkbox"
                  name="time"
                  value="all"
                  checked={selected.length === timeOptions.length}
                  onChange={() => handleSelect("all")}
                />
              </label>
              {renderCheckboxes(timeOptions)}
            </form>
          </>
        ) : (
          <>
            <h3>방송 스타일</h3>
            <form className="form-container">
              <label>
                전체 선택
                <input
                  type="checkbox"
                  name="time"
                  value="all"
                  checked={selected.length === broadcastOptions.length}
                  onChange={() => handleSelect("all")}
                />
              </label>
              {renderCheckboxes(broadcastOptions)}
            </form>
          </>
        )}
      </section>
    </div>
  );
}
