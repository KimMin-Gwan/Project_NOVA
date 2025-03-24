import ScheduleCard from "../../component/EventCard/EventCard";
import React, { useEffect, useState } from "react";
import mainApi from "../../services/apis/mainApi";
import useToggleMore from "../../hooks/useToggleMore";
import "./index.css";
import {
  ScheduleMore,
  ScheduleAdd,
  ScheduleEdit,
  ScheduleRemove,
} from "../../component/ScheduleMore/ScheduleMore";
import BiasBoxes from "../../component/BiasBoxes";

export default function MySchedulePage() {
  let [thisWeekSchedule, setThisWeekSchedule] = useState([]);
  let [mySchedules, setMySchedules] = useState([]);
  let [key, setKey] = useState(-1);
  let [bid, setBid] = useState("");
  const { moreClick, handleToggleMore } = useToggleMore();

  // 이번주 일정 받아오기
  function fetchThisWeekSchedule() {
    mainApi.get("time_table_server/try_get_weekday_schedules").then((res) => {
      setThisWeekSchedule(res.data.body.schedules);
    });
  }

  // bid를 가지고 검색하기
  // 주제 없음에서는 bid 비워서 보내면됨
  function fetchSelectedSchedule() {
    mainApi
      .get(`time_table_server/try_search_my_schedule_with_bid?bid=${bid}&key=${key}`)
      .then((res) => {
        setMySchedules(res.data.body.schedules);
        setKey(res.data.body.key);
      });
  }

  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [targetSchedule, setTargetSchedule] = useState({});

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleAddScheduleModal = (target) => {
    setAddScheduleModal((addScheduleModal) => !addScheduleModal);
    setTargetSchedule(target);
  };

  // 게시판으로 이동
  const navBoard = () => {};

  useEffect(() => {
    fetchThisWeekSchedule();
  }, []);

  useEffect(() => {
    fetchSelectedSchedule();
  }, [bid]);

  return (
    <div className="container MySchedulePage">
      <section className="MySchedule__section">
        <div className="section_header">
          <h3>이번 주 일정</h3>
          <p>대시보드에 표시될 일정입니다.</p>
        </div>

        {thisWeekSchedule.map((item) => {
          return (
            <li key={item.sid}>
              <ScheduleCard
                {...item}
                toggleClick={() => handleToggleMore(item.sid)} // id 전달
              />
              {moreClick[item.sid] &&
                (item.is_already_have === false ? null : item.is_owner === false ? ( // 이미 가지고 있는게 아니면 여기 나올 필요자체가 없음
                  <ScheduleRemove
                    target={item}
                    detailClick={toggleAddScheduleModal}
                    navBoardClick={navBoard}
                  />
                ) : (
                  <ScheduleEdit
                    target={item}
                    detailClick={toggleAddScheduleModal}
                    navBoardClick={navBoard}
                  />
                ))}
            </li>
          );
        })}
      </section>

      <section className="MySchedule__section">
        <div className="section_header">
          <h3>내가 선택한 일정</h3>
        </div>
        <div className="bias_wrapper">
          <BiasBoxes />
        </div>
        {mySchedules.map((item) => {
          return (
            <li key={item.sid}>
              <ScheduleCard
                {...item}
                toggleClick={() => handleToggleMore(item.sid)} // id 전달
              />
              {moreClick[item.sid] &&
                (item.is_already_have === false ? null : item.is_owner === false ? ( // 이미 가지고 있는게 아니면 여기 나올 필요자체가 없음
                  <ScheduleRemove
                    target={item}
                    detailClick={toggleAddScheduleModal}
                    navBoardClick={navBoard}
                  />
                ) : (
                  <ScheduleEdit
                    target={item}
                    detailClick={toggleAddScheduleModal}
                    navBoardClick={navBoard}
                  />
                ))}
            </li>
          );
        })}

        <div className="button_container">
          <button className="moresee_button">더보기</button>
        </div>
      </section>
    </div>
  );
}
