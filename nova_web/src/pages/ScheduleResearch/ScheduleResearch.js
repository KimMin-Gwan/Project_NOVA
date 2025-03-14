import React, { useState } from "react";
import style from "./ScheduleResearch.module.css";
import ScheduleCalendar from "../../component/ScheduleCalendar/ScheduleCalendar";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import ScheduleEvent from "../../component/ScheduleEvent/ScheduleEvent";
import { ScheduleMore } from "../../component/ScheduleMore/ScheduleMore";
import { ScheduleEventMore } from "../../component/EventMore/EventMore";

import { mockData } from "../../pages/SchedulePage/TestScheduleData";
import useToggleMore from "../../component/useToggleMore";

export default function ScheduleResearch() {
  const [isMoreModal, setIsMoreModal] = useState(false);
  const { moreClick, toggleMore } = useToggleMore();

  // 일정번들에 자세히 모달 토글
  const toggleSchedule = () => {
    setIsMoreModal((isMoreModal) => !isMoreModal);
  };

  return (
    <div className={`container  ${style["ScheduleResearch"]}`}>
      <section className={style["eventCalendarBox"]}>
        <nav>
          <h3>이벤트</h3>
          <button>이벤트 직접 추가</button>
        </nav>
        <ScheduleCalendar />
        <ScheduleEvent />
      </section>

      <ScheduleSearch title={2} />

      {mockData.map((item) => (
        <li key={item.id} className={style["eventBox"]}>
          <ScheduleEvent toggleClick={() => toggleMore(item.id)} />
          {moreClick[item.id] && (
            <ScheduleMore scheduleClick={toggleSchedule} />
          )}
        </li>
      ))}

      <ScheduleEventMore closeSchedule={toggleSchedule} isOpen={isMoreModal} />
    </div>
  );
}
