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
  const { moreClick, toggleMore } = useToggleMore();
  const [isModal, setIsModal] = useState(false);
  const navigate = useNavigate();

  // 팔로우 모달창 나오게 하기
  function handleFollowModal() {
    setIsModal((isModal) => !isModal);
  }

  function clickPath(path) {
    navigate(`${path}`);
  }

  return (
    <div className="container SearchSchedulePage">
      <ScheduleSearch
        title={0}
        clickButton={() => clickPath("/search/research")}
      />

      <ul className="scheduleList">
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
