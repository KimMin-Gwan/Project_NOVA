//import { Link, useNavigate } from "react-router-dom";
//import style from "./NoticeList.module.css";
//import backword from "./../../img/back_icon.png";


//function Notice() {
  //let navigate = useNavigate();

  //return (
    //<div className={style["main-body"]}>
      //<div className={style.TopBar}>
        //<img
          //src={backword}
          //alt="Arrow"
          //className={style.backword}
          //onClick={() => {
            //navigate(-1);
          //}}
        ///>
        //<div className={style.TitleBox}>
          //<p className={style.titleName}> 공지사항 </p>
        //</div>
        //<div className={style.EmptyBox} />
      //</div>

      //<div className={style["notice-area"]}>
        //<div className={style.notice}>
          //<p className={style.titleName}>제목 </p>
          //<p className={style.date}>2024/10/7</p>
        //</div>
        //<div className={style["png-area"]}>
          //<p className={style.text}>본문 예시입니다. </p>
        //</div>
      //</div>
    //</div>
  //);
//}

//export default Notice;


import React, { useState, useEffect } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom"; // Import useLocation for accessing navigation state
import style from "./NoticeList.module.css";
import backword from "./../../img/back_icon.png";

function Notice() {
  const navigate = useNavigate();
  const { nid } = useParams(); // Get 'nid' from URL
  const location = useLocation(); // Access additional data passed via state
  const [notice, setNotice] = useState(null); // State to store notice details
  const [loading, setLoading] = useState(true); // Loading state
  //const nid = location.state.nid


  useEffect(() => {
    fetchNoticeDetail();
  }, [nid]);

  const fetchNoticeDetail = async () => {
    try {
      const response = await fetch(`https://nova-platform.kr/nova_notice/notice_detail?nid=${nid}`);
      if (!response.ok) {
        throw new Error("Failed to fetch notice details");
      }
      const data = await response.json();
      setNotice(data.body.notice); // Assuming the API returns the notice object
      setLoading(false);
    } catch (error) {
      console.error("Error fetching notice detail:", error);
      setLoading(false);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  }

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
        {notice ? (
          <>
            <div className={style.notice}>
              <p className={style.titleName}>{notice.title}</p>
              <p className={style.date}>{notice.date}</p>
            </div>
            <div className={style["png-area"]}>
              <p className={style.text}>
                {notice.body.split('\n').map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </p>
            </div>
          </>
        ) : (
          <p>Notice not found</p>
        )}
      </div>
    </div>
  );
}

export default Notice;
