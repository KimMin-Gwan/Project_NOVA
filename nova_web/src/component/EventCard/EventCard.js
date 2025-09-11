import style from "./EventCard.module.css";

export default function ScheduleCard({
  title,
  uname,
  update_time,
  bname,
  datetime,
  location,
  code,
  toggleClick,
  selectBack,
}) {

  const { formattedDate, formattedTime } = formatDateTime(datetime);

  return (
    <div
      className={style["EventCard"]}
      onClick={toggleClick}
      style={{ backgroundColor: selectBack }}
    >
      <dl>
        <span className={style["EventHeader"]}>
          <dt>{title}</dt>
          <section className={style["UnameInfo"]}>
            <dt>{uname} 등록</dt>
            <dt>{update_time}</dt>
          </section>
        </span>
        <section className={style["DesInfo"]}>
          <section className={style["BnameInfo"]}>
            <dt>{bname}</dt>
            <dt>
              {formattedDate} | {formattedTime}
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

function formatDateTime(dateStr) {
  const date = new Date(dateStr);

  // 날짜
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  // 요일
  const weekDays = ["일", "월", "화", "수", "목", "금", "토"];
  const week = weekDays[date.getDay()];

  const formattedDate = `${month}월 ${day}일 ${week}`;

  // 시간
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const ampm = hours >= 12 ? "오후" : "오전";
  hours = hours % 12;
  hours = hours ? hours : 12; // 0 -> 12
  const formattedTime = `${ampm} ${String(hours).padStart(2,"0")}:${minutes}`;

  return { formattedDate, formattedTime };
}