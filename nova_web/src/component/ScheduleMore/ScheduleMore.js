import { BUTTON_TYPES } from "../../constant/type_data";
import style from "./ScheduleMore.module.css";

const BUTTON_SETTING = {
  [BUTTON_TYPES.DEFAULT]: { first: "", second: "게시판", last: "자세히" },
  [BUTTON_TYPES.SELECT]: { first: "", second: "일정 선택하기", last: "모두 추가하기" },
  [BUTTON_TYPES.SCHEDULE]: { first: "자세히", second: "게시판에서 공유", last: "추가하기" },
  [BUTTON_TYPES.BIAS]: { first: "게시판", second: "일정 검색", last: "팔로우" },
  [BUTTON_TYPES.CANCEL]: { first: "", second: "선택 취소", last: "선택한 일정 추가하기" },
  [BUTTON_TYPES.EVENT]: { first: "", second: "", last: "이벤트 추가하기" },
  [BUTTON_TYPES.SCHEDULE_HAVE]: { first: "", second: "게시판에서 공유", last: "일정에서 제외하기" },
  [BUTTON_TYPES.SCHEDULE_EDIT]: { first: "", second: "게시판에서 공유", last: "수정하기" },
};

function BasicSchedule({ isMore, firstClick, secondClick, lastClick, target }) {
  const buttons = BUTTON_SETTING[isMore];

  function isLastButtonClicked() {
    lastClick(target);
  }

  function isFistButtonClicked() {
    firstClick(target);
  }

  return (
    <div className={style["moreContainer"]}>
      {buttons.first !== "" && (
        <button onClick={isFistButtonClicked} className={style["moreButton"]}>
          {buttons.first}
        </button>
      )}
      {buttons.second !== "" && <button onClick={secondClick}>{buttons.second}</button>}
      <button onClick={isLastButtonClicked}>{buttons.last}</button>
    </div>
  );
}
// 일정 번들 밑에 붙는 버튼
export function ScheduleMore({ navBoardClick, scheduleClick, target }) {
  return (
    <BasicSchedule
      isMore={BUTTON_TYPES.DEFAULT}
      target={target}
      secondClick={navBoardClick}
      lastClick={scheduleClick}
    />
  );
}
// 일정 번들 자세히보기 모달창에서 밑에 붙는 버튼
export function ScheduleDetailAdd({ selectToggle, selectText, allSelect }) {
  return <BasicSchedule isMore={selectText} secondClick={selectToggle} lastClick={allSelect} />;
}
// 일정 밑에 붙는 버튼
export function ScheduleAdd({ navBoardClick, detailClick, addClick, target}) {
  return (
    <BasicSchedule
      isMore={BUTTON_TYPES.SCHEDULE}
      target={target}
      firstClick={detailClick}
      secondClick={navBoardClick}
      lastClick={addClick}
    />
  );
}

// 일정 밑에 붙는 버튼
export function ScheduleRemove({ navBoardClick, detailClick, addClick, target}) {
  return (
    <BasicSchedule
      isMore={BUTTON_TYPES.SCHEDULE_HAVE}
      target={target}
      firstClick={detailClick}
      secondClick={navBoardClick}
      lastClick={addClick}
    />
  );
}

// 일정 밑에 붙는 버튼
export function ScheduleEdit({ navBoardClick, detailClick, addClick, target}) {
  return (
    <BasicSchedule
      isMore={BUTTON_TYPES.SCHEDULE_EDIT}
      target={target}
      firstClick={detailClick}
      secondClick={navBoardClick}
      lastClick={addClick}
    />
  );
}

// 주제 탐색 페이지의 버튼
export function ScheduleFollow({ scheduleClick, followClick, target }) {
  return (
    <BasicSchedule
      isMore={BUTTON_TYPES.BIAS}
      target={target}
      secondClick={scheduleClick}
      lastClick={followClick}
    />
  );
}
// 스케줄 이벤트 추가하기 버튼
export function ScheduleEventAdd() {
  return <BasicSchedule isMore={BUTTON_TYPES.EVENT} />;
}
