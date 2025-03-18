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
export default function ScheduleTopic({
  bname,
  category,
  agency,
  tags,
  main_time,
  toggleClick,
}) {
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
            <dd>
              {//tags.map((item, index) => {
                //return (
                  //<p key={index}>
                    //{item}
                    //{index !== tags.length - 1 && ","}
                  //</p>
                //);
              //})
              <p>{tags}</p>
              }
            </dd>
          </span>
          <span className={style["MainTime"]}>
            <dt>주 방송 시간</dt>
            <dd>
              {
              //main_time.map((item, index) => {
                //return (
                  //<p key={index}>
                    //{item}
                    //{index !== main_time.length - 1 && ","}
                  //</p>
                //);
              //})
              <p>{main_time}</p>
              }
            </dd>
          </span>
        </section>
      </dl>

      <div className={style["bias_img"]}>img</div>
    </div>
  );
}
