import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Swiper, SwiperSlide } from "swiper/react";
import { Scrollbar } from "swiper/modules";
import "swiper/css";
import "swiper/css/scrollbar";
import back from "./../../img/detail_back.png";
import useToggleMore from "../../hooks/useToggleMore";
import HEADER from "../../constant/header";
import postApi from "../../services/apis/mainApi";


import "./index.css";
import useIntersectionObserver from "../../hooks/useIntersectionObserver";
import NoneSchedule from "../../component/NoneFeed/NoneSchedule";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";

import ScheduleExploreDesktop from "./ScheduleExplore.jsx";
import ScheduleComponentMobile from "./ScheduleComponentMobile.jsx";
import ScheduleDetailMobile from "../../component/ScheduleDetail/ScheduleDetailMobile.jsx";
const scheduleKind = ["게임", "저챗", "음악", "그림", "스포츠", "시참"];

export default function ScheduleExplore() {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const navigate = useNavigate();

  const [modalButton, setModalButton] = useState(false);

  const swiperRef = useRef(null);

  const [activeIndex, setActiveIndex] = useState(0);
  const [targetCategory, setTargetCategory] = useState(scheduleKind[activeIndex]);

  const [buttonType, setButtonType] = useState("");
  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  // 누르면 키가 자꾸 올라가는 문제가 있음 !!!!
  const handleClick = (index) => {
    setActiveIndex(index);
    swiperRef.current.swiper.slideTo(index);
  };

  function handleModal(type) {
    setModalButton((modalButton) => !modalButton);
    setButtonType(type);
  }

  // 슬라이드 변경 시 활성화된 탭을 동기화
  const handleTabChange = (swiper) => {
    setActiveIndex(swiper.activeIndex);
  };


  const [showScheduleMoreOption, setShowScheduleMoreOption] = useState(false);
  const [targetSchedule, setTargetSchedule] = useState("");

  const toggleDetailOption = (targetSchedule) => {
      setTargetSchedule(targetSchedule);
      setShowScheduleMoreOption(!showScheduleMoreOption);
  }


  if(isMobile){
  return (
    <div className="container ExploreSchedulePage">

      {
          showScheduleMoreOption && 
          <ScheduleDetailMobile
              sid={targetSchedule}
              toggleDetailOption={toggleDetailOption}
          />
      }
      <nav className="navBar">
        <button onClick={() => navigate(-1)} className="backButton">
          <img src={back} alt="" />
        </button>
        <h1>일정 탐색</h1>
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
      <Swiper
        spaceBetween={50}
        slidesPerView={1}
        onSlideChange={handleTabChange}
        ref={swiperRef}
        className="scheduleList"
      >
        <ul>
          <ul>
            {scheduleKind.map((item, index) => (
              <SwiperSlide key={index}>
                <ScheduleComponentList
                  isMobile={isMobile}
                  category={item}
                  toggleDetailOption={toggleDetailOption}
                  activeIndex={activeIndex}
                  setActiveIndex={setActiveIndex}
                  myIndex={index}
                />
              </SwiperSlide>
            ))}
          </ul>
        </ul>
      </Swiper>
      <ButtonModal
        closeSchedule={handleModal}
        isOpen={modalButton}
        type={buttonType}
      />
    </div>
  );
  }else{
    return(
      <DesktopLayout>
        <ScheduleComponentList
          isMobile={isMobile}
          category={targetCategory}
          setCategory={setTargetCategory}
          activeIndex={activeIndex}
          setActiveIndex={setActiveIndex}
          myIndex={0}
        />
      </DesktopLayout>
    )
  }
}



function ScheduleComponentList({
  isMobile, category, setCategory, toggleDetailOption,
   activeIndex, setActiveIndex, myIndex
}){

  const [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);
  const [scheduleData, setScheduleData] = useState([]);
  const [key, setKey] = useState(-1);
  const [isInit, setIsInit] = useState(false);
  const { moreClick, handleToggleMore } = useToggleMore();
  const loadMoreCallBack = () => {
    if (!isLoading && hasMore) {
      fetchMoreSearchData()
    }
  };
  const targetRef = useIntersectionObserver(loadMoreCallBack, { threshold: 0.5 }, hasMore);

  const navigate = useNavigate();
  // 게시판으로 이동
  const navBoard = (target) => {
    navigate(`/search_result?keyword=${target}`);
  };

  async function fetchSearchData() {
    console.log("1");
    await postApi
      .post("time_table_server/get_explore_schedules", {
        header: HEADER,
        body: {
          category: category,
          key:key,
          time_section: -1,
          style: "all",
          gender : "all"
        },
      })
      .then((res) => {
        setScheduleData(res.data.body.schedules);
        setHasMore(res.data.body.schedules.length > 0);
        setKey(res.data.body.key);
        setIsLoading(false);
        setIsInit(true);
      });
  }

  async function fetchMoreSearchData() {
    console.log("2");
    await postApi
      .post("time_table_server/get_explore_schedules", {
        header: HEADER,
        body: {
          category: category,
          key:key,
          time_section: -1,
          style: "all",
          gender : "all"
        },
      })
      .then((res) => {
        setScheduleData((prev) => [...prev, ...res.data.body.schedules]);
        setHasMore(res.data.body.schedules.length > 0);
        setKey(res.data.body.key);
      });
  }

  useEffect(() => {
    if (isMobile){
      if (!isInit) {
        //if (scheduleData.length ===0){
          if (activeIndex== myIndex){
            fetchSearchData();
            setIsInit(true);
          }
        //}
      }
    }else{
      fetchSearchData();
      setIsInit(true);
    }

  }, [activeIndex]);

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryAddSchedule(target) {
    // 무조건 리스트로 만들어야됨
    const sids = [target.sid];

    await postApi
      .post("time_table_server/try_add_schedule", {
        header: HEADER,
        body: {
          sids: sids,
        },
      })
      .then((res) => {
        setScheduleData((prev) => {
          if (!prev.some((item) => item.sid === target.sid)) {
            // 목표 item이 없으면 기존 상태 반환
            return prev;
          }
          // 목표 item이 있으면 업데이트
          return prev.map((item) =>
            item.sid === target.sid ? { ...item, subscribe: true } : item
          );
        });
      });
  }


  if(isMobile){
    return (
      <>
        {scheduleData.length === 0 && <NoneSchedule/>}


        {scheduleData.map((singleSchedule, index) => (
          <ScheduleComponentMobile
            key={index}
            toggleDetailOption={toggleDetailOption}
            {...singleSchedule}
          />
          ))}
          <div ref={targetRef} style={{ height: "1px" }}></div>
      </>
    );
  }else{
    return(
      <ScheduleExploreDesktop 
        setCategory={setCategory}
        activeIndex={activeIndex}
        setActiveIndex={setActiveIndex}
        scheduleData={scheduleData}
        fetchMoreSearchData={fetchMoreSearchData}
        setKey={setKey}
      />
    );
  }
}





// Tabs 컴포넌트가 존재, 그거랑 합치기 필요
function TabItem({ tabs, activeIndex, handleClick }) {
  const tabRefs = React.useRef([]);

  const handleTabClick = (index, tab) => {
    handleClick(index, tab);

    // 해당 탭으로 스크롤 이동
    tabRefs.current[index]?.scrollIntoView({
      behavior: "smooth",
      inline: "center",
    });
  };

  return (
    <>
      {tabs.map((tab, index) => (
        <li
          key={index}
          className={`post ${activeIndex === index ? "active" : ""}`}
          onClick={() => handleTabClick(index, tab)}
          ref={(el) => (tabRefs.current[index] = el)}
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
