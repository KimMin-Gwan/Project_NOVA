import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import style from "./SearchTopicPage.module.css";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ScheduleFollow } from "../../component/ScheduleMore/ScheduleMore";
import ScheduleFollowBox from "../../component/ScheduleFollowBox/ScheduleFollowBox";
import { mockData } from "../../pages/SchedulePage/TestScheduleData";
import useToggleMore from "../../component/useToggleMore";



export default function SearchTopicPage() {
  let [eventData, setEventData] = useState([]);

  const { moreClick, toggleMore } = useToggleMore();
  const [isModal, setIsModal] = useState(false);
  const navigate = useNavigate();

  //// 오늘짜 이벤트 데이터 받아오고
  //// 이것도 나중에 오늘 말고 내일, 이틀 후 사흘 후 이런걸로 해야될 듯
  //function fetchEventData() {
    //mainApi.get("time_table_server/try_get_event_board_data").then((res) => {
      //setEventData(res.data.body.schedule_events);
    //});
  //}

  // 팔로우 모달창 나오게 하기
  function handleFollowModal() {
    setIsModal((isModal) => !isModal);
  }

  function clickPath(path) {
    navigate(`${path}`);
  }

  return (
    <div className={`container ${style["SearchTopicPage"]}`}>
      <ScheduleSearch
        title={0}
        clickButton={() => clickPath("/search/research")}
      />

      <ul className={style["scheduleList"]}>
        {mockData.map((item) => (
          <li key={item.id}>
            <ScheduleTopic
              key={item.id}
              toggleClick={() => toggleMore(item.id)}
            />
            {moreClick[item.id] && (
              <ScheduleFollow
                scheduleClick={() => clickPath("/search/schedule")}
                followClick={handleFollowModal}
              />
            )}
          </li>
        ))}
      </ul>

      {isModal && <ScheduleFollowBox closeModal={handleFollowModal} />}
    </div>
  );
}
