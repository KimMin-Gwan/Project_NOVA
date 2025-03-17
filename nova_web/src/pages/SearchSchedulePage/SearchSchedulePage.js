import ScheduleCard from "../../component/EventCard/EventCard";
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
import { BundleScheduleDetail, EventDetail, ScheduleDetail} from "../../component/EventMore/EventMore";
import mainApi from "../../services/apis/mainApi";

export default function SearchSchedulePage() {
  const typeSelectData = ["schedule_bundle", "schedule", "event"];

  const [activeIndex, setActiveIndex] = useState(0);
  const [ScheduleIndex, setScheduleIndex] = useState(0);
  const { moreClick, toggleMore } = useToggleMore();

  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [addScheduleBundleModal, setAddScheduleBundleModal] = useState(false);
  const [addEventModal, setAddEventMoal] = useState(false);

  const [scheduleBundleData, setScheduleBundleData] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);
  const [scheduleEventData, setScheduleEventData] = useState([]);

  const [scheduleBundleKey, setScheduleBundleKey] = useState(-1);
  const [scheduleKey, setScheduleKey] = useState(-1);
  const [scheduleEventKey, setScheduleEventKey] = useState(-1);

  const [typeSelect, setTypeSelect] = useState("schedule_bundle");

  const [keyword, setKeyword] = useState("");

  const [hasMore, setHasMore] = useState(false);

  const navigate = useNavigate();

  async function fetchSearchData(keyword) {
    if (activeIndex == 0 ){
      await mainApi
        .get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleBundleKey}&type=${typeSelectData[activeIndex]}`)
        .then((res) => {
          setScheduleBundleData((prev) => [...prev, ...res.data.body.schedule_bundles]);
          setScheduleBundleKey(res.data.body.key);
      });
    }
    else if (activeIndex == 1) {
      await mainApi
        .get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleKey}&type=${typeSelectData[activeIndex]}`)
        .then((res) => {
          setScheduleData((prev) => [...prev, ...res.data.body.schedules]);
          setScheduleKey(res.data.body.key);
      });
    }
    else if (activeIndex == 2) {
      await mainApi
        .get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleEventKey}&type=${typeSelectData[activeIndex]}`)
        .then((res) => {
          setScheduleEventData((prev) => [...prev, ...res.data.body.schedule_events]);
          setScheduleEventKey(res.data.body.key);
      });
    }
  }

  useEffect(() => {
    fetchSearchData("");
  }, []);
  
  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  const handleClick = (index, type) => {
    setActiveIndex(index);
    setScheduleIndex(index);
    setTypeSelect(typeSelectData[index])
    fetchSearchData("");
  };

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleAddScheduleModal = () => {
    setAddScheduleModal((addScheduleModal) => !addScheduleModal);
  };

  // 일정 번들 추가하기 버튼 누르면 동작하는 애
  const toggleAddScheduleBundleModal= () => {
    setAddScheduleBundleModal((addScheduleBundleModal) => !addScheduleBundleModal);
  };

  // 이벤트 추가하기 버트 ㄴ누르면 동작하는 애
  const toggleAddEventModal= () => {
    setAddEventMoal((addEventModal) => !addEventModal);
  };

  // 게시판으로 이동
  const navBoard = () => {
    console.log("클릭");
    navigate("/");
  };

  const ScheduleKind = ["일정 번들", "일정", "이벤트"];

  return (
    <div className="container SearchSchedulePage">
      <ScheduleSearch title={1} fetchMockData={fetchSearchData} />
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
          ? scheduleBundleData.map((item) => (
              <li key={item.id}>
                <ScheduleBundle
                  key={item.id}
                  item={item}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && (
                  <ScheduleMore
                    navBoardClick={navBoard}
                    scheduleClick={toggleAddScheduleBundleModal}
                  />
                )}
              </li>
            ))
          : ScheduleIndex === 1
          ? scheduleData.map((item) => (
              <li>
                <ScheduleCard
                  key={item.id}
                  {...item}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && <ScheduleAdd
                    navBoardClick={navBoard}
                    scheduleClick={toggleAddEventModal}
                 />}
              </li>
            ))
          : scheduleEventData.map((item) => (
              <li>
                <ScheduleEvent
                  key={item.id}
                  {...item}
                  toggleClick={() => toggleMore(item.id)}
                />
                {moreClick[item.id] && <ScheduleMore 
                    navBoardClick={navBoard}
                    scheduleClick={toggleAddScheduleModal}
                />}
              </li>
            ))}
      </ul>

      <BundleScheduleDetail closeSchedule={toggleAddScheduleBundleModal} isOpen={addScheduleBundleModal} />
      <EventDetail closeSchedule={toggleAddEventModal} isOpen={addEventModal} />
      <ScheduleDetail closeSchedule={toggleAddScheduleModal} isOpen={addScheduleModal} />
    </div>
  );
}
