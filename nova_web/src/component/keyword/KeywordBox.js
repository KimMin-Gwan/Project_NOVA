import style from "./KeywordBox.module.css";

export default function KeywordBox({ title, subTitle }) {
  return (
    <div className={style["keyword-container"]}>
      <div className={style["title-container"]}>
        {title} <span className={style["sub-title"]}>{subTitle}</span>
      </div>

      <div className={style["tags-container"]}>
        <div className={style["tags"]}>#tags</div>
        <div className={style["tags"]}>tags</div>
        <div className={style["tags"]}>tags</div>
        <div className={style["tags"]}>tagddddds</div>
        <div className={style["tags"]}>tagddddds</div>
        <div className={style["tags"]}>tagddddds</div>
      </div>
      <div className={style["tags-container"]}>
        <div className={style["tags-wrapper"]}>
          <div className={style["tags"]}>#tags</div>
          <div className={style["tags"]}>tags</div>
          <div className={style["tags"]}>tags</div>
          <div className={style["tags"]}>tagddddds</div>
          <div className={style["tags"]}>tagddddds</div>
          <div className={style["tags"]}>tagddddds</div>
        </div>
      </div>
    </div>
  );
}
