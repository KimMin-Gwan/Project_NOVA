import style from "./EventCard.module.css";
import { schedule } from "../../pages/SchedulePage/TestScheduleData";

export default function ScheduleCard({
  detail,
  uname,
  update_time,
  bname,
  start_date,
  start_time,
  location,
  code,
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
          <dt>{detail}</dt>
          <section className={style["UnameInfo"]}>
            <dt>{uname} 등록</dt>
            <dt>{update_time}</dt>
          </section>
        </span>
        <section className={style["DesInfo"]}>
          <section className={style["BnameInfo"]}>
            <dt>{bname}</dt>
            <dt>
              {start_date} | {start_time}
            </dt>
            <dt>{location}</dt>
          </section>
          <span className={style["CodeInfo"]}>
            <p>일정 코드</p>
            <div>{code}</div>
          </span>
        </section>
      </dl>
    </div>
  );
}
