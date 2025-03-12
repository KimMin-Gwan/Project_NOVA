import style from "./ScheduleEvent.module.css";
import { event } from "../../pages/SchedulePage/TestScheduleData";

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
