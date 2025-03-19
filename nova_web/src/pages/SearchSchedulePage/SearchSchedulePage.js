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
import postApi from "../../services/apis/mainApi";
import HEADER from "../../constant/header";


export default function SearchSchedulePage() {
  //const typeSelectData = ["schedule_bundle", "schedule", "event"];
  //const [addEventModal, setAddEventMoal] = useState(false);

  const typeSelectData = ["schedule_bundle", "schedule"];

  const [activeIndex, setActiveIndex] = useState(0);
  const [ScheduleIndex, setScheduleIndex] = useState(0);

  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [addScheduleBundleModal, setAddScheduleBundleModal] = useState(false);

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

  const [moreClick, setMoreClick] = useState({});
//  const { moreClick, setMoreClick} = useToggleMore();
  function toggleMore(id){
    setMoreClick((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const [moreClickBundle, setMoreClickBundle] = useState({});
  function toggleMoreBundle(id){
    setMoreClickBundle((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  async function fetchSearchData(keyword) {
    // setActiveIndex가 너무 느리게 동작해서 그냥 index를 파라미터로 받아서 만들게 했습니다
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
    // Event는 1.5버전에 추가 예정
    //else if (activeIndex == 2) {
      //await mainApi
        //.get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleEventKey}&type=${typeSelectData[activeIndex]}`)
        //.then((res) => {
          //setScheduleEventData((prev) => [...prev, ...res.data.body.schedule_events]);
          //setScheduleEventKey(res.data.body.key);
      //});
    //}
  }

  async function fetchSearchDataWidthIndex(keyword, index) {
    // setActiveIndex가 너무 느리게 동작해서 그냥 index를 파라미터로 받아서 만들게 했습니다
    if (index== 0 ){
      await mainApi
        .get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleBundleKey}&type=${typeSelectData[index]}`)
        .then((res) => {
          setScheduleBundleData((prev) => [...prev, ...res.data.body.schedule_bundles]);
          setScheduleBundleKey(res.data.body.key);
      });
    }
    else if (index== 1) {
      await mainApi
        .get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleKey}&type=${typeSelectData[index]}`)
        .then((res) => {
          setScheduleData((prev) => [...prev, ...res.data.body.schedules]);
          setScheduleKey(res.data.body.key);
      });
    }
    // Event는 1.5버전에 추가 예정
    //else if (activeIndex == 2) {
      //await mainApi
        //.get(`time_table_server/try_search_schedule_with_keyword?keyword=${keyword}&key=${scheduleEventKey}&type=${typeSelectData[activeIndex]}`)
        //.then((res) => {
          //setScheduleEventData((prev) => [...prev, ...res.data.body.schedule_events]);
          //setScheduleEventKey(res.data.body.key);
      //});
    //}
  }

  useEffect(() => {
    fetchSearchData("");
  }, []);
  
  // 일정 탐색 페이지에 일정번들, 일정, 이벤트 상태 변경
  // 누르면 키가 자꾸 올라가는 문제가 있음 !!!!
  const handleClick = (index, type) => {
    setActiveIndex(index);
    setScheduleIndex(index);
    setTypeSelect(typeSelectData[index])
    fetchSearchDataWidthIndex("", index);
  };

  const [targetSchedule, setTargetSchedule] = useState({});
  const [targetScheduleBundle, setTargetScheduleBundle] = useState({});

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleAddScheduleModal = (target) => {
    setAddScheduleModal((addScheduleModal) => !addScheduleModal);
    setTargetSchedule(target)
  };


  // 일정 번들 추가하기 버튼 누르면 동작하는 애
  const toggleAddScheduleBundleModal= (target) => {
    setAddScheduleBundleModal((addScheduleBundleModal) => !addScheduleBundleModal);
    setTargetScheduleBundle(target)
  };

  //// 이벤트 추가하기 버트 ㄴ누르면 동작하는 애
  //const toggleAddEventModal= () => {
    //setAddEventMoal((addEventModal) => !addEventModal);
  //};

  // 게시판으로 이동
  const navBoard = () => {
    console.log("클릭");
    navigate("/");
  };

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryAddSchedule(target) {
    // 무조건 리스트로 만들어야됨
    const sids = [target.sid]

    await postApi 
      .post('time_table_server/try_add_schedule', {
      header: HEADER,
      body: {
        sids: sids,
      }})
  }; 

  //const ScheduleKind = ["일정 번들", "일정", "이벤트"];
  const ScheduleKind = ["일정 번들", "일정"];

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
                <li key={item.sbid}>
                  <ScheduleBundle
                    item={item}
                    toggleClick={() => toggleMoreBundle(item.sbid)} // id 전달
                  />
                  {moreClickBundle[item.sbid] && ( // 해당 id의 상태만 확인
                    <ScheduleMore
                      target={item}
                      navBoardClick={navBoard}
                      scheduleClick={toggleAddScheduleBundleModal}
                    />
                  )}
                </li>
              ))
            : scheduleData.map((item) => (
                <li key={item.sid}>
                  <ScheduleCard
                    {...item}
                    toggleClick={() => toggleMore(item.sid)} // id 전달
                  />
                  {moreClick[item.sid] && ( // 해당 id의 상태만 확인
                    <ScheduleAdd
                      target={item}
                      detailClick={toggleAddScheduleModal}
                      navBoardClick={navBoard}
                      addClick={fetchTryAddSchedule}
                    />
                  )}
                </li>
              ))}
        </ul>

      {/* 자세히 보기 모달창 */}
      <BundleScheduleDetail closeSchedule={toggleAddScheduleBundleModal} isOpen={addScheduleBundleModal} target={targetScheduleBundle} />

      {/*여기도 target 추가해야될 듯 */}
      <ScheduleDetail closeSchedule={toggleAddScheduleModal} isOpen={addScheduleModal} target={targetSchedule} />
    </div>
  );
}


      //<EventDetail closeSchedule={toggleAddEventModal} isOpen={addEventModal} />

          //? scheduleData.map((item) => (
              //<li>
                //<ScheduleCard
                  //key={item.id}
                  //{...item}
                  //toggleClick={() => toggleMore(item.id)}
                ///>
                //{moreClick[item.id] && <ScheduleAdd
                    //navBoardClick={navBoard}
                    //scheduleClick={toggleAddEventModal}
                 ///>}
              //</li>
            //))
          //: scheduleEventData.map((item) => (
              //<li>
                //<ScheduleEvent
                  //key={item.id}
                  //{...item}
                  //toggleClick={() => toggleMore(item.id)}
                ///>
                //{moreClick[item.id] && <ScheduleMore 
                    //navBoardClick={navBoard}
                    //scheduleClick={toggleAddScheduleModal}
                ///>}
              //</li>
            //))