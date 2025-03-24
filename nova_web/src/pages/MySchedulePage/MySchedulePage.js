import ScheduleCard from "../../component/EventCard/EventCard";
import React, { useEffect, useState } from "react";
import mainApi from "../../services/apis/mainApi";
import useToggleMore from "../../hooks/useToggleMore";
import { ScheduleMore, ScheduleAdd, ScheduleEdit, ScheduleRemove } from "../../component/ScheduleMore/ScheduleMore";

export default function MySchedulePage() {
  let [thisWeekSchedule, setThisWeekSchedule] = useState([]);
  let [mySchedules, setMySchedules] = useState([]);
  let [key, setKey] = useState(-1)
  let [bid, setBid] = useState("")
  const { moreClick, handleToggleMore } = useToggleMore();

 // 이번주 일정 받아오기
  function fetchThisWeekSchedule() {
    mainApi.get('time_table_server/try_get_weekday_schedules').then((res) => {
      setThisWeekSchedule(res.data.body.schedules);
    });
  }

  // bid를 가지고 검색하기
  // 주제 없음에서는 bid 비워서 보내면됨
  function fetchSelectedSchedule() {
    mainApi.get(`time_table_server/try_search_my_schedule_with_bid?bid=${bid}&key=${key}`).then((res) => {
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
  const navBoard = () => {
  };


  useEffect(()=>{
    fetchThisWeekSchedule()
  }, [])

  useEffect(()=>{
    fetchSelectedSchedule()
  }, [bid])

  // 모양 볼려면 여기로 보삼
  // 테스트용 계정
  // id : testUser@naver.com
  // password : sample122
  console.log(thisWeekSchedule)
  console.log(mySchedules)


  return (
    <div className="container">
      <section>
        <div>이벤트 추가</div>

        { thisWeekSchedule.map((item) => {
          <li key={item.sid}>
            <ScheduleCard
              {...item}
              toggleClick={() => handleToggleMore(item.sid)} // id 전달
            />
            {moreClick[item.sid] && (
              item.is_already_have === false ? (
                // 이미 가지고 있는게 아니면 여기 나올 필요자체가 없음
                null
              ) : item.is_owner === false? (
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
              )
            )}
          </li>
        })}
      </section>

      <section>
        <div>내가 선택한 일정</div>

        <div>일정</div>
      </section>

      <div>더보기</div>
    </div>
  );
}
