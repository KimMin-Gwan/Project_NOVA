import style from "./ScheduleTopic.module.css";

export default function ScheduleTopic({ bname, category, agency, tags, main_time, toggleClick }) {
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

      <div className={style["bias_img"]}>img</div>
    </div>
  );
}
