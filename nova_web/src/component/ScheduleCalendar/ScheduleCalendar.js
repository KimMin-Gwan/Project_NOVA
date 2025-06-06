import React, { useState } from "react";
import Calendar from "react-calendar";
import moment from "moment";
import "react-calendar/dist/Calendar.css";
import { sampleDate } from "../../pages/SchedulePage/TestScheduleData";
import "./index.css";
export default function ScheduleCalendar() {
  const data = sampleDate;

  const [value, onChange] = useState(new Date());

  const tileClassName = ({ date }) => {
    if (date.getDay() === 0 || date.getDay() == 6) {
      return "weekend";
    }
  };
  return (
    <section className="CalendarBox">
      <Calendar
        onChange={onChange}
        value={value}
        showNeighboringMonth={false}
        calendarType="hebrew"
        formatDay={(locale, date) => moment(date).format("D")}
        tileClassName={tileClassName}
        tileContent={({ date, view }) => {
          if (data.find((x) => x === moment(date).format("YYYY-MM-DD"))) {
            return (
              <>
                <div className="dotContainer">
                  <div className="dot"></div>
                </div>
              </>
            );
          }
        }}
      />
    </section>
  );
}
