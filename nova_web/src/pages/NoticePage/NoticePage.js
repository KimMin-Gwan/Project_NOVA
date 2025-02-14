import { useNavigate } from "react-router-dom";
import "./index.css";

export default function NoticePage() {
  const navigate = useNavigate();
  return (
    <div className="NoticePage">
      <div className="NoticePage_title">
        <button
          onClick={() => {
            navigate(-1);
          }}
        >
          돌아가기
        </button>
        <div>공지사항</div>
      </div>

      <hr className="hr-line" />

      <section className="notice_container">
        <div className="notice_title">
          <p>#공지사항 제목</p>
          <h6>공지 일자</h6>
        </div>
        <hr className="hr-line hr-line-in-box" />

        <div className="notice_content">공지사항 본문</div>
      </section>

      <hr className="hr-line" />

      <div className="notice_container last_notice">마지막 공지사항입니다.</div>
    </div>
  );
}
