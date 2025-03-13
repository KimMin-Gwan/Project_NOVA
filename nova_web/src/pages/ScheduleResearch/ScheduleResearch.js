import React, { useState } from "react";
import style from "./ScheduleResearch.module.css";
import ScheduleCalendar from "../../component/ScheduleCalendar/ScheduleCalendar";

export default function ScheduleResearch() {
  return (
    <div className={`container  ${style["ScheduleResearch"]}`}>
      <nav>
        <h3>이벤트</h3>
      </nav>
      <ScheduleCalendar />
    </div>
  );
}
