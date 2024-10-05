import { Link, useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";
import style from "./NoticeList.module.css";

function NoticeList() {
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
        <div
          className={style.noticelist}
          onClick={() => {
            navigate("/notice");
          }}
        >
          <span className={style.noticeText}>공지사항 1</span>
        </div>
        <div
          className={style.noticelist}
          onClick={() => {
            navigate("/notice");
          }}
        >
          <span className={style.noticeText}>공지사항 2</span>
        </div>
        <div
          className={style.noticelist}
          onClick={() => {
            navigate("/notice");
          }}
        >
          <span className={style.noticeText}>공지사항 3</span>
        </div>
      </div>
    </div>
  );
}

export default NoticeList;
