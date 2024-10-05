import { Link, useNavigate } from "react-router-dom";
import style from "./NoticeList.module.css";
import backword from "./../../img/back_icon.png";
function Notice() {
  let navigate = useNavigate();
  return (
    <div className={style["main-body"]}>
      <div className={style.TopBar}>
        <img
          src={backword}
          alt="Arrow"
          className={style.backword}
          onClick={() => {
            navigate(-1);
          }}
        />
        <div className={style.TitleBox}>
          <p className={style.titleName}> 공지사항 </p>
        </div>
        <div className={style.EmptyBox} />
      </div>

      <div className={style["notice-area"]}>
        <div className={style.notice}>
          <p className={style.titleName}>제목 </p>
          <p className={style.date}>2024/10/7</p>
        </div>
        <div className={style["png-area"]}>
          <p className={style.text}>본문 예시입니다. </p>
        </div>
      </div>
    </div>
  );
}

export default Notice;
