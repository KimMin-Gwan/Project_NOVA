import React, { useState } from "react";
import style from "./ScheduleResearch.module.css";
import ScheduleCalendar from "../../component/ScheduleCalendar/ScheduleCalendar";
import ScheduleSearch from "../../component/ScheduleSearch/ScheduleSearch";
import ScheduleEvent from "../../component/ScheduleEvent/ScheduleEvent";
import { ScheduleMore } from "../../component/ScheduleMore/ScheduleMore";

export default function ScheduleResearch() {
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
      <div className={style["eventBox"]}>
        <ScheduleEvent />
        <ScheduleMore />
      </div>
    </div>
  );
}
