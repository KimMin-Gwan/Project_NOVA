import style from "./ScheduleMore.module.css";

function BasicSchedule({ isMore, followClick }) {
  return (
    <div className={style["moreContainer"]}>
      {isMore && (
        <button className={style["moreButton"]}>
          {isMore === 1 ? "자세히" : "게시판"}
        </button>
      )}
      <button>
        {isMore ? (isMore === 1 ? "게시판에서 공유" : "일정 검색") : "게시판"}
      </button>
      <button onClick={followClick}>
        {isMore ? (isMore === 1 ? "추가하기" : "팔로우") : "자세히"}
      </button>
    </div>
  );
}

export function ScheduleMore() {
  return <BasicSchedule />;
}

export function ScheduleAdd() {
  return <BasicSchedule isMore={1} />;
}

export function ScheduleFollow({ followClick }) {
  return <BasicSchedule isMore={2} followClick={followClick} />;
}
