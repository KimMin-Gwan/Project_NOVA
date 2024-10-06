import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import backword from "./../../img/back_icon.png";
import style from "./NoticeList.module.css";

function NoticeList() {
  const navigate = useNavigate();
  const [notices, setNotices] = useState([]);

  useEffect(() => {
    fetchNotices();
  }, []);

  const fetchNotices = async () => {
    try {
      const response = await fetch("https://nova-platform.kr/nova_notice/notice_list");
      if (!response.ok) {
        throw new Error("Failed to fetch notices");
      }
      const data = await response.json();
      setNotices(data.body.notice_list); // Assuming data is an array of notices
    } catch (error) {
      console.error("Error fetching notices:", error);
      // Handle error fetching data (e.g., show error message)
    }
  };
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
            <p className={style.titleName}>공지사항</p>
          </div>
          <div className={style.EmptyBox} />
        </div>

        <div className={style["notice-area"]}>
          {notices.map((notice, index) => (
            <div
              key={index}
              className={style.noticelist}
              onClick={() => {
                navigate(`/notice/${notice.nid}`);
              }}
            >
              <span className={style.noticeText}>{notice.title}</span>
              <span className={style.noticeDate}>(      {notice.date})</span> {/* Display the date next to title */}
            </div>
          ))}
        </div>
      </div>
    );
}

export default NoticeList;


