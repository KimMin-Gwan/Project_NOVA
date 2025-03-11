import search_icon from "./../../img/search_icon.png";
import arrow from "./../../img/home_arrow.svg";
import style from "./ScheduleSearch.module.css";
const keyword = {
  word: ["인터넷방송", "유튜버", "버튜버"],
};

export default function ScheduleSearch() {
  return (
    <div className={style["SearchSection"]}>
      <div className={style["sectionTop"]}>
        <h3>일정 탐색</h3>
        <button>일정 등록</button>
      </div>
      <div className={style["searchFac"]}>
        <div className={style["searchBox"]}>
          <input
            type="text"
            //   onKeyDown={onKeyDown}
            //   value={searchBias}
            //   onChange={(e) => {
            //     onChangeSearchBias(e);
            //   }}
            placeholder="키워드 또는 일정 코드를 입력해 보세요!"
          />
          <img
            src={search_icon}
            // onClick={fetchSearchBias}
            alt="검색바"
          />
        </div>
      </div>
      <section className={style["wordSection"]}>
        <img src={arrow} alt="화살표" />
        {keyword.word.map((item, key) => {
          return <button key={item}>{item}</button>;
        })}
      </section>
    </div>
  );
}
