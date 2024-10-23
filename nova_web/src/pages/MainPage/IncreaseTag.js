import style from "./MainPart.module.css";

export default function IncreaseTag() {
  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header>급상승 해시태그</header>
          {/* <div>화살표</div> */}
        </div>
      </div>

      <div className={style["main-area"]}>
        <div className={style["hashtag-box"]}>
          <span className={style["time-text"]}>13:00 기준</span>
          <ol className={style["ranking-container"]}>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>1위</div>
              <div className={style["ranking-name"]}># 에스파</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>2위</div>
              <div className={style["ranking-name"]}># 경민생카</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>3위</div>
              <div className={style["ranking-name"]}># 조슈아생일시</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>4위</div>
              <div className={style["ranking-name"]}># Mantra</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>5위</div>
              <div className={style["ranking-name"]}># 제니</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>6위</div>
              <div className={style["ranking-name"]}># 오뱅온</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>7위</div>
              <div className={style["ranking-name"]}># 지스타</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>8위</div>
              <div className={style["ranking-name"]}># 숲인방</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>9위</div>
              <div className={style["ranking-name"]}># 버추얼하꼬</div>
            </li>
            <li className={style["ranking-box"]}>
              <div className={style["ranking"]}>10위</div>
              <div className={style["ranking-name"]}># 가을야구</div>
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
}
