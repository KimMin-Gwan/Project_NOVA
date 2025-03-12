import EventCard from "../../component/EventCard/EventCard";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import ScheduleEvent from "../../component/ScheduleEvent/ScheduleEvent";
import "./index.css";
import ScheduleBundle from "../../component/ScheduleEvent/ScheduleBundle";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import React, { useEffect, useRef, useState } from "react";
import {
  ScheduleMore,
  ScheduleAdd,
} from "../../component/ScheduleMore/ScheduleMore";
import EventMore from "../../component/EventMore/EventMore";

const mockData = [
  {
    id: 0,
    name: "한결",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
  {
    id: 1,
    name: "한결1",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
  {
    id: 2,
    name: "한결2",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
];

const ScheduleKind = ["일정 번들", "일정", "이벤트"];

// const eventData = [
//   {
//     id: 0,
//     name: "한결 3월 1주차 방송 스케줄",
//     topic: "한결",
//     date: "25년 03월 01일",
//   },
//   {
//     id: 1,
//     name: "플레이브 미니 3집",
//     topic: "플레이브",
//     date: "25년 03월 01일",
//   },
//   {
//     id: 2,
//     name: "한결 3월 1주차 방송 스케줄",
//     topic: "한결1",
//     date: "25년 03월 01일",
//   },
// ];

export default function SearchSchedulePage() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [ScheduleIndex, setScheduleIndex] = useState(0);
  const [moreClick, setMoreClick] = useState({});
  const [isMoreModal, setIsMoreModal] = useState(false);
  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  const handleClick = (index, type) => {
    setActiveIndex(index);
    setScheduleIndex(index);
  };

  // 클릭시 버튼 보이게 해주기
  const toggleMore = (id) => {
    setMoreClick((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // 일정번들에 자세히 모달 토글
  const toggleSchedule = () => {
    setIsMoreModal((isMoreModal) => !isMoreModal);
  };

  return (
    <div className="container SearchSchedulePage">
      <ScheduleSearch title={true} />
      <section className={"info-list"}>
        <ul className={"post-list"} data-active-index={activeIndex}>
          {ScheduleKind.map((item, index) => (
            <li
              key={item}
              className={`post ${activeIndex === index ? "active" : ""}`}
              onClick={() => handleClick(index, item)}
            >
              <button>{item}</button>
            </li>
          ))}
        </ul>
      </section>
      <ul className="scheduleList">
        {ScheduleIndex === 0
          ? mockData.map((item) => (
              <li>
                <ScheduleBundle
                  key={item.id}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && (
                  <ScheduleMore scheduleClick={toggleSchedule} />
                )}
              </li>
            ))
          : ScheduleIndex === 1
          ? mockData.map((item) => (
              <li>
                <EventCard
                  key={item.id}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && <ScheduleAdd />}
              </li>
            ))
          : mockData.map((item) => (
              <li>
                <ScheduleEvent
                  key={item.id}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && <ScheduleMore />}
              </li>
            ))}
      </ul>

      <EventMore closeSchedule={toggleSchedule} isOpen={isMoreModal} />
    </div>
  );
}
