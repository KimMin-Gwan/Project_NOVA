import style from "./ScheduleMore.module.css";

function BasicSchedule({ isMore, lastclick }) {
  const buttons = [
    {
      first: "",
      second: "게시판",
      last: "자세히",
    },
    {
      first: "자세히",
      second: "게시판에서 공유",
      last: "추가하기",
    },
    {
      first: "게시판",
      second: "일정 검색",
      last: "팔로우",
    },
  ];

  return (
    <div className={style["moreContainer"]}>
      {isMore > 0 && (
        <button className={style["moreButton"]}>{buttons[isMore].first}</button>
      )}
      <button>{buttons[isMore].second}</button>
      <button onClick={lastclick}>{buttons[isMore].last}</button>
    </div>
  );
}

export function ScheduleMore({ scheduleClick }) {
  return <BasicSchedule isMore={0} lastclick={scheduleClick} />;
}

export function ScheduleAdd({ addClick }) {
  return <BasicSchedule isMore={1} lastclick={addClick} />;
}

export function ScheduleFollow({ followClick }) {
  return <BasicSchedule isMore={2} lastclick={followClick} />;
}
