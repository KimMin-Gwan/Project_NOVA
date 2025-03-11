import style from "./ScheduleEvent.module.css";

const schedule_bundle = {
  sbid: "121t-5t91-9ana", // schedule bundle id
  sbname: "한결 3월 1주차 방송 스케줄",
  bid: "1005",
  bname: "한결", // bias_name
  location: ["SOOP"],
  date: ["25년 03월 01일", "25년 03월 08일"],
  sids: ["1235-0agf-1251", "t215-gh2h-11rc"],
  uid: "1111-abcd-2222",
  uname: "허니과메기",
};

export default function ScheduleBundle({ toggleClick }) {
  return (
    <div className={style["ScheduleEvent"]} onClick={toggleClick}>
      <dl>
        <span className={style["ScheduleBudleTitle"]}>
          <dt>{schedule_bundle.sbname}</dt>
          <p>{schedule_bundle.uname} 등록</p>
        </span>
        <dt>{schedule_bundle.bname}</dt>
        <dt>
          {schedule_bundle.date.map((item, index) => {
            return (
              <p key={index}>
                {item} {index == 0 && "-"}
              </p>
            );
          })}
        </dt>
      </dl>
    </div>
  );
}
