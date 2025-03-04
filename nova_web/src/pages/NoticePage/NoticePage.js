import { useNavigate } from "react-router-dom";
import "./index.css";
import mainApi from "../../services/apis/mainApi";
import { useEffect, useState } from "react";

export default function NoticePage() {
  const navigate = useNavigate();

  const [notices, setNotices] = useState([]);

  function fetchNotice() {
    mainApi.get("nova_sub_system/sample_notice").then((res) => {
      //console.log(res.data);
      setNotices(res.data.body.notice);
    });
  }

  useEffect(() => {
    fetchNotice();
  }, []);

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

      {notices.map((notice, i) => {
        return (
          <section key={notice.nid} className="notice_container">
            <div className="notice_title">
              <p>{notice.title}</p>
              <h6>{notice.date}</h6>
            </div>
            <hr className="hr-line hr-line-in-box" />

            <div className="notice_content">{notice.body}</div>
          </section>
        );
      })}

      <hr className="hr-line" />

      <div className="notice_container last_notice">마지막 공지사항입니다.</div>
    </div>
  );
}
