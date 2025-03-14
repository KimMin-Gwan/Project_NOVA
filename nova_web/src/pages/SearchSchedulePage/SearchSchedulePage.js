import EventCard from "../../component/EventCard/EventCard";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import ScheduleEvent from "../../component/ScheduleEvent/ScheduleEvent";
import "./index.css";
import { ScheduleBundle } from "../../component/ScheduleEvent/ScheduleBundle";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import useToggleMore from "../../component/useToggleMore";
import { useNavigate } from "react-router-dom";
import React, { useEffect, useRef, useState } from "react";
import {
  ScheduleMore,
  ScheduleAdd,
} from "../../component/ScheduleMore/ScheduleMore";
import { BundleEventMore } from "../../component/EventMore/EventMore";

import {
  mockData,
  ScheduleKind,
} from "../../pages/SchedulePage/TestScheduleData";
import TestRef from "../../component/TestRef";

export default function SearchSchedulePage() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [ScheduleIndex, setScheduleIndex] = useState(0);
  const { moreClick, toggleMore } = useToggleMore();
  const [isMoreModal, setIsMoreModal] = useState(false);
  const navigate = useNavigate();

  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  const handleClick = (index, type) => {
    setActiveIndex(index);
    setScheduleIndex(index);
  };

  // 일정번들에 자세히 모달 토글
  const toggleSchedule = () => {
    setIsMoreModal((isMoreModal) => !isMoreModal);
  };
  // 게시판으로 이동
  const navBoard = () => {
    console.log("클릭");
    navigate("/");
  };

  return (
    <div className="container SearchSchedulePage">
      <ScheduleSearch title={1} />
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
              <li key={item.id}>
                <ScheduleBundle
                  key={item.id}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && (
                  <ScheduleMore
                    navBoardClick={navBoard}
                    scheduleClick={toggleSchedule}
                  />
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

      <BundleEventMore closeSchedule={toggleSchedule} isOpen={isMoreModal} />
    </div>
  );
}
