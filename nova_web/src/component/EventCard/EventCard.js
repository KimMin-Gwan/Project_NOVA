import style from "./EventCard.module.css";
import { schedule } from "../../pages/SchedulePage/TestScheduleData";

export default function EventCard({
  name,
  topic,
  date,
  toggleClick,
  selectBack,
}) {
  return (
    <div
      className={style["EventCard"]}
      onClick={toggleClick}
      style={{ backgroundColor: selectBack }}
    >
      <dl>
        <span className={style["EventHeader"]}>
          <dt>{schedule.detail}</dt>
          <section className={style["UnameInfo"]}>
            <dt>{schedule.uname} 등록</dt>
            <dt>{schedule.update_time}</dt>
          </section>
        </span>
        <section className={style["DesInfo"]}>
          <section className={style["BnameInfo"]}>
            <dt>{schedule.bname}</dt>
            <dt>
              {schedule.date} | {schedule.start}
            </dt>
            <dt>{schedule.location}</dt>
          </section>
          <span className={style["CodeInfo"]}>
            <p>일정 코드</p>
            <div>{schedule.code}</div>
          </span>
        </section>
      </dl>
    </div>
  );
}
