import ScheduleTopic from "../../component/ScheduleTopic/ScheduleTopic";
import style from "./SearchTopicPage.module.css";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import React, { useEffect, useRef, useState } from "react";
import { ScheduleFollow } from "../../component/ScheduleMore/ScheduleMore";
import ScheduleFollowBox from "../../component/ScheduleFollowBox/ScheduleFollowBox";
import { mockData } from "../../pages/SchedulePage/TestScheduleData";

export default function SearchTopicPage() {
  const [moreClick, setMoreClick] = useState({});
  const [isModal, setIsModal] = useState(false);

  // 주제 탐색 페이지에 누르면 버튼 나오게 하기
  const toggleMore = (id) => {
    setMoreClick((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // 팔로우 모달창 나오게 하기
  function handleFollowModal() {
    setIsModal((isModal) => !isModal);
  }

  return (
    <div className="container SearchSchedulePage">
      <ScheduleSearch title={0} />

      <ul className="scheduleList">
        {mockData.map((item) => (
          <li>
            <ScheduleTopic
              key={item.id}
              toggleClick={() => toggleMore(item.id)}
            />
            {moreClick[item.id] && (
              <ScheduleFollow followClick={handleFollowModal} />
            )}
          </li>
        ))}
      </ul>

      {isModal && <ScheduleFollowBox closeModal={handleFollowModal} />}
    </div>
  );
}
