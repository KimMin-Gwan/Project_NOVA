import style from "./ScheduleResearch.module.css";
import Calendar from "react-calendar";
export default function ScheduleResearch() {
  return (
    <div className={`container  ${style["ScheduleResearch"]}`}>
      <section>
        <Calendar />
      </section>
    </div>
  );
}
