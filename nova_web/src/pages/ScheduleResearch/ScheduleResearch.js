import React, { useState } from "react";
import style from "./ScheduleResearch.module.css";
import ScheduleCalendar from "../../component/ScheduleCalendar/ScheduleCalendar";

export default function ScheduleResearch() {
  return (
    <div className={`container  ${style["ScheduleResearch"]}`}>
      <section>
        <ScheduleCalendar />
      </section>
    </div>
  );
}
