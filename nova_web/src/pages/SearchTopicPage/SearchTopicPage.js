import EventCard from "../../component/EventCard/EventCard";
import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import ScheduleEvent from "../../component/ScheduleEvent/ScheduleEvent";
import style from "./SearchTopicPage.module.css";
import ScheduleBundle from "../../component/ScheduleEvent/ScheduleBundle";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import React, { useEffect, useRef, useState } from "react";
import {
  ScheduleMore,
  ScheduleAdd,
} from "../../component/ScheduleMore/ScheduleMore";

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

export default function SearchTopicPage() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [ScheduleIndex, setScheduleIndex] = useState(0);
  const [moreClick, setMoreClick] = useState({});

  const handleClick = (index, type) => {
    setActiveIndex(index);
    setScheduleIndex(index);
  };

  const toggleMore = (id) => {
    setMoreClick((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  return (
    <div className="container SearchSchedulePage">
      <ScheduleSearch />

      <ul className="scheduleList">
        {ScheduleIndex === 0
          ? mockData.map((item) => (
              <li>
                <ScheduleBundle
                  key={item.id}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && <ScheduleMore />}
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
    </div>
  );
}
