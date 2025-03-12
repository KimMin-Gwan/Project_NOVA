import style from "./ScheduleEvent.module.css";
import { schedule_bundle } from "../../pages/SchedulePage/TestScheduleData";

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
