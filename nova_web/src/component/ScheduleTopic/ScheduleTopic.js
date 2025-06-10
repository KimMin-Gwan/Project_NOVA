import style from "./ScheduleTopic.module.css";
import tempBias from "./../../img/tempBias.png";

export default function ScheduleTopic({ bid, bname, category, agency, tags, main_time, toggleClick }) {
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  return (
    <div className={style["ScheduleTopic"]} onClick={toggleClick}>
      <dl>
        <section className={style["BiasTitle"]}>
          <dt>{bname}</dt>
          <dt>{category}</dt>
        </section>

        <section className={style["BiasMain"]}>
          <dt>{agency}</dt>

          <span className={style["TagSt"]}>
            <dt>태그</dt>
            <dd>{<p>{tags}</p>}</dd>
          </span>

          <span className={style["MainTime"]}>
            <dt>주 방송 시간</dt>
            <dd>{<p>{main_time}</p>}</dd>
          </span>
        </section>
      </dl>

      <div className={style["bias_img"]}>
        <img
          src={bias_url + `${bid}.png`}
          alt="bias"
          onError={(e) => (e.target.src = tempBias)}
        />
      </div>
    </div>
  );
}

export function ScheduleTopicMain({ bid, bname, category, agency, tags, main_time, toggleClick }) {
  let bias_url = "https://kr.object.ncloudstorage.com/nova-images/";

  return (
    <div className={style["ScheduleTopicMain"]} onClick={toggleClick}>
      <dl>
        <section className={style["BiasTitle"]}>
          <dt>{bname}</dt>
          <dt>{category}</dt>
        </section>

        <section className={style["BiasMain"]}>
          <dt>{agency}</dt>

          <span className={style["TagSt"]}>
            <dt>태그</dt>
            <dd>{<p>{tags}</p>}</dd>
          </span>

          <span className={style["MainTime"]}>
            <dt>주 방송 시간</dt>
            <dd>{<p>{main_time}</p>}</dd>
          </span>
        </section>
      </dl>

      <div className={style["bias_img"]}>
        <img
          src={bias_url + `${bid}.png`}
          alt="bias"
          onError={(e) => (e.target.src = tempBias)}
        />
      </div>
    </div>
  );
}