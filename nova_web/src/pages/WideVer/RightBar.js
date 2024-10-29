import style from "./WideVer.module.css";
import style_hash from "./../MainPage/MainPart.module.css";
import { useNavigate } from "react-router-dom";
export default function RightBar() {
  return (
    <div className={style["wrap_container"]}>
      <div className={style_hash["hashtag-box"]}>
        <div className={style["top-bar"]}>
          <header className={style["wide-text"]}>급상승 해시태그</header>
          <span className={style_hash["time-text"]}>13:00 기준</span>
        </div>
        <ol className={style_hash["ranking-container"]}>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>1위</div>
            <div className={style_hash["ranking-name"]}># 에스파</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>2위</div>
            <div className={style_hash["ranking-name"]}># 경민생카</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>3위</div>
            <div className={style_hash["ranking-name"]}># 조슈아생일시</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>4위</div>
            <div className={style_hash["ranking-name"]}># Mantra</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>5위</div>
            <div className={style_hash["ranking-name"]}># 제니</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>6위</div>
            <div className={style_hash["ranking-name"]}># 오뱅온</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>7위</div>
            <div className={style_hash["ranking-name"]}># 지스타</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>8위</div>
            <div className={style_hash["ranking-name"]}># 숲인방</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>9위</div>
            <div className={style_hash["ranking-name"]}># 버추얼하꼬</div>
          </li>
          <li className={style_hash["ranking-box"]}>
            <div className={style_hash["ranking"]}>10위</div>
            <div className={style_hash["ranking-name"]}># 가을야구</div>
          </li>
        </ol>
      </div>

      <div className={style["ad-container"]}>광고</div>
    </div>
  );
}
