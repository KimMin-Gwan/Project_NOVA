import style from "./ScheduleMore.module.css";

function BasicSchedule({ isMore }) {
  return (
    <div className={style["moreContainer"]}>
      {isMore && <button className={style["moreButton"]}>자세히</button>}
      <button>{isMore ? "게시판에서 공유" : "게시판"}</button>
      <button>{isMore ? "추가하기" : "자세히"}</button>
    </div>
  );
}

export function ScheduleMore() {
  return <BasicSchedule />;
}

export function ScheduleAdd() {
  return <BasicSchedule isMore={true} />;
}
