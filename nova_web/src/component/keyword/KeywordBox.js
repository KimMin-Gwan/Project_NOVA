import Slider from "react-slick";
import style from "./KeywordBox.module.css";

export default function KeywordBox({ title, subTitle }) {
  const data = ["t", "ta", "tags", "tags", "tags", "tags", "tags", "tags", "tags", "tagssss"];
  const copyFirst = data[0];
  const last = data[data.length - 1];
  const copy = [copyFirst, ...data, last];

  return (
    <div className={style["keyword-container"]}>
      <div className={style["title-container"]}>
        {title} <span className={style["sub-title"]}>{subTitle}</span>
      </div>

      <div className={style["tags-container"]}>
        <div className={style["tags-wrapper"]}>
          {copy.map((datas, i) => {
            return (
              <div key={i} className={style["tags"]}>
                #{datas}
              </div>
            );
          })}
        </div>
      </div>
      {/* <div className={style["tags-container"]}>
        <div className={style["tags-wrapper"]}>
          <div className={style["tags"]}>tags</div>
          <div className={style["tags"]}>tags</div>
          <div className={style["tags"]}>tagddddds</div>
          <div className={style["tags"]}>tagddddds</div>
          <div className={style["tags"]}>tagddddddddddddddddssssss</div>
        </div>
      </div> */}
    </div>
  );
}
