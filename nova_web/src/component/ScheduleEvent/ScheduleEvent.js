import style from "./ScheduleEvent.module.css";
import { event } from "../../pages/SchedulePage/TestScheduleData";

export default function ScheduleEvent({ sename, bname, date, location, start, toggleClick }) {
  return (
    <div className={style["ScheduleEvent"]} onClick={toggleClick}>
      <dl>
        <dt>{sename}</dt>
        <dt>{bname}</dt>
        <dt>
          {location},{date},{start}
        </dt>
      </dl>
    </div>
  );
}
