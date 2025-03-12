import style from "./ScheduleMore.module.css";

function BasicSchedule({ isMore, secondClick, lastClick }) {
  const buttons = [
    {
      first: "",
      second: "게시판",
      last: "자세히",
    },
    {
      first: "",
      second: "일정 선택하기",
      last: "모두 추가하기",
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
    {
      // 버튼 토글 시
      first: "",
      second: "선택 취소",
      last: "선택한 일정 추가하기",
    },
  ];

  return (
    <div className={style["moreContainer"]}>
      {buttons[isMore].first !== "" && (
        <button className={style["moreButton"]}>{buttons[isMore].first}</button>
      )}
      <button onClick={secondClick}>{buttons[isMore].second}</button>
      <button onClick={lastClick}>{buttons[isMore].last}</button>
    </div>
  );
}
// 일정 번들 버튼
export function ScheduleMore({ scheduleClick }) {
  return <BasicSchedule isMore={0} lastClick={scheduleClick} />;
}
// 일정 번들 자세히보기 버튼
export function ScheduleMoreAdd({ selectToggle, selectText, allSelect }) {
  return (
    <BasicSchedule
      isMore={selectText}
      secondClick={selectToggle}
      lastClick={allSelect}
    />
  );
}
// 일정 버튼
export function ScheduleAdd({ addClick }) {
  return <BasicSchedule isMore={2} lastClick={addClick} />;
}
// 주제 탐색 페이지의 버튼
export function ScheduleFollow({ followClick }) {
  return <BasicSchedule isMore={3} lastClick={followClick} />;
}
