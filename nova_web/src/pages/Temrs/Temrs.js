import { Link, useNavigate } from "react-router-dom";
import style from "./Termslist.module.css";
import backword from "./../../img/back_icon.png";

function Terms() {
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
          <p className={style.titleName}> 이용약관 </p>
        </div>
        <div className={style.EmptyBox} />
      </div>

      <div className={style["notice-area"]}>
        <div
          className={style.noticelist}
          onClick={() => {
            navigate("/service_terms_and_conditions.pdf");
          }}
        >
          <span className={style.noticeText}>개인정보처리방침</span>
        </div>
        <div
          className={style.noticelist}
          onClick={() => {
            navigate("/personal_information_processing_policy.pdf");
          }}
        >
          <span className={style.noticeText}>개인정보처리동의서</span>
        </div>
        <div
          className={style.noticelist}
          onClick={() => {
            navigate("/personal_information_processing_agreement.pdf");
          }}
        >
        </div>
      </div>
    </div>
  );
}

export default Terms;
