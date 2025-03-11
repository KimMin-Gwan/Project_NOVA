import style from "./ScheduleEvent.module.css";

const event = {
  seid: "1234-abcd-5678", // schedule event id
  sename: "플레이브 미니 3집 Caligo Pt.1 발매",
  bid: "1008",
  bname: "플레이브", // bias_name
  location: ["Yes24"],
  date: "03월 04일",
  start: "오후 06:00",
  end: "오후 08:00",
  sids: ["1235-0agf-1251", "t215-gh2h-11rc"],
  uid: "1111-abcd-2222",
  uname: "허니과메기",
};

export default function ScheduleEvent({ name, topic, date, toggleClick }) {
  return (
    <div className={style["ScheduleEvent"]} onClick={toggleClick}>
      <dl>
        <dt>{event.sename}</dt>
        <dt>{event.bname}</dt>
        <dt>
          {event.location},{event.date},{event.start}
        </dt>
      </dl>
    </div>
  );
}
