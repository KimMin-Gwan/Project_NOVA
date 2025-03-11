import style from "./ScheduleTopic.module.css";
const bias = {
  bid: "1008", // bias id
  bname: "허니츄러스", // bias_name
  category: "인터넷 방송인", // bias category
  agency: "치지직", //소속
  tags: ["신입", "버츄얼", "치지직", "스트리머"],
  main_time: ["저녁", "새벽"],
  is_ad: false,
};
export default function ScheduleTopic({ name, job, tag, platform, time }) {
  return (
    <div className={style["ScheduleTopic"]}>
      <dl>
        <section className={style["BiasTitle"]}>
          <dt>{bias.bname}</dt>
          <dt>{bias.category}</dt>
        </section>
        <section className={style["BiasMain"]}>
          <dt>{bias.agency}</dt>
          <span className={style["TagSt"]}>
            <dt>태그</dt>
            <dd>
              {bias.tags.map((item, index) => {
                return (
                  <p key={index}>
                    {item}
                    {index !== bias.tags.length - 1 && ","}
                  </p>
                );
              })}
            </dd>
          </span>
          <span className={style["MainTime"]}>
            <dt>주 방송 시간</dt>
            <dd>
              {bias.main_time.map((item, index) => {
                return (
                  <p key={index}>
                    {item}
                    {index !== bias.main_time.length - 1 && ","}
                  </p>
                );
              })}
            </dd>
          </span>
        </section>
      </dl>

      <div className={style["bias_img"]}>img</div>
    </div>
  );
}
