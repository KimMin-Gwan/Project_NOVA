import style from "./EventCard.module.css";
const schedule = {
  sid: "1235-0agf-11tr", // schedule id
  detail: "1부 저챗, 2부 사과게임 켠왕", // schedule detail
  bid: "1008", // bias id
  bname: "허니츄러스", // bias_name
  uid: "1111-abcd-2222", // 작성자 id
  uname: "허니과메기", //작성자 이름
  start: "오후 06:00",
  end: "오후 08:00",
  date: "03월 04일",
  update_time: "3시간 전",
  location: "치지직",
  code: "ABCDEFG",
  color_code: "#FF0000",
};

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
