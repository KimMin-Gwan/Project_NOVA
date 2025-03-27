import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import back from "./../../img/detail_back.png";
import arrow from "./../../img/explore_down.png";
import useToggleMore from "../../hooks/useToggleMore";

import mainApi from "../../services/apis/mainApi";
import "./index.css";
import style from "../../component/EventMore/EventMore.module.css";

import ModalRectangle from "./../../img/ModalRectangle.png";

export default function ScheduleExplore() {
  const { moreClick, handleToggleMore } = useToggleMore();
  const navigate = useNavigate();

  const [modalButton, setModalButton] = useState(false);

  let [searchKeyword, setSearchKeyword] = useState("");

  const typeSelectData = ["schedule_bundle", "schedule"];
  const scheduleKind = ["게임", "저챗", "음악", "그림", "스포츠", "시참"];

  const [activeIndex, setActiveIndex] = useState(0);

  // 모달
  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [addScheduleBundleModal, setAddScheduleBundleModal] = useState(false);
  const [makeScheduleModal, setMakeScheduleModal] = useState(false);
  const [editScheduleModal, setEditScheduleModal] = useState(false);

  // 키 값
  const [scheduleBundleKey, setScheduleBundleKey] = useState(-1);
  const [scheduleKey, setScheduleKey] = useState(-1);

  useEffect(() => {
    setScheduleKey(-1);
    setScheduleBundleKey(-1);
  }, [searchKeyword, activeIndex]);

  // 탭 변경시 검색 초기화
  useEffect(() => {
    setSearchKeyword("");
    setScheduleBundleKey(-1);
  }, [activeIndex]);

  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  // 누르면 키가 자꾸 올라가는 문제가 있음 !!!!
  const handleClick = (index) => {
    setActiveIndex(index);
  };

  // 게시판으로 이동
  const navBoard = () => {
    navigate("/");
  };

  function handleModal() {
    setModalButton((modalButton) => !modalButton);
  }
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
      <section className="button-container">
        <button onClick={handleModal}>
          시간 설정 <img src={arrow} alt="" />
        </button>
        <button>
          방송 스타일 <img src={arrow} alt="" />
        </button>
        <button>
          성별 <img src={arrow} alt="" />
        </button>
      </section>
      <ul className="scheduleList"></ul>
      <ButtonModal closeSchedule={handleModal} isOpen={modalButton} />
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

export function ButtonModal({ closeSchedule, isOpen, children }) {
  const [backgroundColor, setBackgroundColor] = useState("");
  const [displaySt, setdisplaySt] = useState("");
  const [upAnimation, setUpAnimation] = useState(false);
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
        {children}
      </section>
    </div>
  );
}
