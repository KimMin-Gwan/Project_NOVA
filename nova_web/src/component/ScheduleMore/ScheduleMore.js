import style from "./ScheduleMore.module.css";

function BasicSchedule({ isMore, firstClick, secondClick, lastClick, target }) {
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
    {
      first: "",
      second: "",
      last: "이벤트 추가하기",
    },
  ];

  function isLastButtonClicked(){
    lastClick(target)
  }

  function isFistButtonClicked(){
    firstClick(target)
  }

  return (
    <div className={style["moreContainer"]}>
      {buttons[isMore].first !== "" && (
        <button onClick={isFistButtonClicked} className={style["moreButton"]}>{buttons[isMore].first}</button>
      )}
      {buttons[isMore].second !== "" && (
        <button onClick={secondClick}>{buttons[isMore].second}</button>
      )}
      <button onClick={isLastButtonClicked}>{buttons[isMore].last}</button>
    </div>
  );
}
// 일정 번들 밑에 붙는 버튼
export function ScheduleMore({ navBoardClick, scheduleClick, target }) {
  return (
    <BasicSchedule
      isMore={0}
      target={target}
      secondClick={navBoardClick}
      lastClick={scheduleClick}
    />
  );
}
// 일정 번들 자세히보기 모달창에서 밑에 붙는 버튼
export function ScheduleDetailAdd({ selectToggle, selectText, allSelect }) {
  return (
    <BasicSchedule
      isMore={selectText}
      secondClick={selectToggle}
      lastClick={allSelect}
    />
  );
}
// 일정 밑에 붙는 버튼
export function ScheduleAdd({ navBoardClick, detailClick, addClick, target }) {
  return <BasicSchedule
      isMore={2}
      target={target}
      firstClick={detailClick}
      secondClick={navBoardClick}
      lastClick={addClick}
       />;
}
// 주제 탐색 페이지의 버튼
export function ScheduleFollow({ scheduleClick, followClick, target }) {
  return (
    <BasicSchedule
      isMore={3}
      target={target}
      secondClick={scheduleClick}
      lastClick={followClick}
    />
  );
}
// 스케줄 이벤트 추가하기 버튼
export function ScheduleEventAdd() {
  return <BasicSchedule isMore={5} />;
}
