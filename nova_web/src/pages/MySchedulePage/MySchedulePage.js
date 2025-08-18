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
import BiasBoxes from "../../component/BiasBoxes/BiasBoxes";

export default function MySchedulePage() {
  let [thisWeekSchedule, setThisWeekSchedule] = useState([]);
  let [mySchedules, setMySchedules] = useState([]);
  let [key, setKey] = useState(-1);
  let [bid, setBid] = useState("");

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

  // 내 스케줄에 등록하는 함수 (추가하기 버튼 누르면 동작해야됨)
  // 완료하면 성공했다고 알려주면 좋을듯
  async function fetchTryRejectSchedule(target) {
    // 무조건 리스트로 만들어야됨
    await mainApi
      .get(`time_table_server/try_reject_from_my_schedule?sid=${target.sid}`)
      .then((res) => {
        setThisWeekSchedule((prev) => (prev ? prev.filter((item) => item.sid !== target.sid) : []));
        setMySchedules((prev) => (prev ? prev.filter((item) => item.sid !== target.sid) : []));
      });
  }

  const [addScheduleModal, setAddScheduleModal] = useState(false);
  const [targetSchedule, setTargetSchedule] = useState({});

  // 일정 추가하기 버튼 누르면 동작하는애
  const toggleAddScheduleModal = (target) => {
    setAddScheduleModal(!addScheduleModal);
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
            <ScheduleItem
              key={item.sid}
              schedule={item}
              toggleAddScheduleModal={toggleAddScheduleModal}
              navBoard={navBoard}
              fetchTryRejectSchedule={fetchTryRejectSchedule}
            />
          );
        })}
      </section>

      <section className="MySchedule__section">
        <div className="section_header">
          <h3>내가 추가한 일정</h3>
        </div>
        <div className="bias_wrapper">
          <BiasBoxes />
        </div>
        {mySchedules.map((item) => {
          return (
            <ScheduleItem
              key={item.sid}
              schedule={item}
              toggleAddScheduleModal={toggleAddScheduleModal}
              navBoard={navBoard}
              fetchTryRejectSchedule={fetchTryRejectSchedule}
            />
          );
        })}

        <div className="button_container">
          <button className="moresee_button">더보기</button>
        </div>
      </section>
    </div>
  );
}

function ScheduleItem({ schedule, toggleAddScheduleModal, navBoard, fetchTryRejectSchedule }) {
  const { moreClick, handleToggleMore } = useToggleMore();

  return (
    <li key={schedule.sid}>
      <ScheduleCard
        {...schedule}
        toggleClick={() => handleToggleMore(schedule.sid)} // id 전달
      />
      {moreClick[schedule.sid] &&
        (schedule.subscribe === false ? null : schedule.is_owner === false ? ( // 이미 가지고 있는게 아니면 여기 나올 필요자체가 없음
          <ScheduleRemove
            target={schedule}
            detailClick={toggleAddScheduleModal}
            navBoardClick={navBoard}
            removeClick={fetchTryRejectSchedule}
          />
        ) : (
          <ScheduleEdit
            target={schedule}
            detailClick={toggleAddScheduleModal}
            navBoardClick={navBoard}
          />
        ))}
    </li>
  );
}
