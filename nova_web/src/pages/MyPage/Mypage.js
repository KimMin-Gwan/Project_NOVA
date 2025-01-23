import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import style from "./Mypage.module.css";
import backword from "./../../img/back_icon.png";
import MyEdit from "./../MyPage/MypageEdit";
import axios from "axios";
import Feed from "../../component/feed";
function MyPage() {
  let navigate = useNavigate();

  let [isLoading, setIsLoading] = useState(true);
  let [myData, setMyData] = useState();

  async function fetchMyPage() {
    await axios
      .get("https://nova-platform.kr/user_home/get_my_page_data", {
        withCredentials: true,
      })
      .then((res) => {
        console.log("my", res.data);
        setMyData(res.data.body);
        setIsLoading(false);
      });
  }

  // let img = `https://kr.object.ncloudstorage.com/nova-user-profile/${myData?.uid}.png`;

  useEffect(() => {
    fetchMyPage();
  }, []);

  async function fetchMyFeed() {
    await axios
      .get(`https://nova-platform.kr/user_home/get_my_feed?type=post&key=-1`, {
        withCredentials: true,
      })
      .then((res) => {
        console.log("feeed", res.data);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchMyFeed();
  }, []);

  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

  const [activeIndex, setActiveIndex] = useState(null);

  const handleClick = (index) => {
    setActiveIndex(index);
  };

  if (isLoading) {
    return <div>loading...</div>;
  }

  return (
    <div className={style.container}>
      <div className={style.top_area}>
        <p
          className={style.backword}
          onClick={() => {
            navigate(-1);
          }}
        >
          뒤로
        </p>
      </div>
      <div className={style["user-container"]}>
        <div className={style["user-img"]}>
          <img
            src={`https://kr.object.ncloudstorage.com/nova-user-profile/${myData.uid}.png`}
            alt="img"
          />
        </div>
        <div>
          <section className={style["user-name"]}>
            <h3>{myData.uname}</h3>
            <img
              src={backword}
              alt=""
              onClick={(e) => handleMovePage(e, "/mypage_edit")} // 클릭 시 /yourPage로 이동
              style={{ cursor: "pointer" }}
            />
          </section>
          <section className={style["user-info"]}>
            <ul>
              <li>
                <b>{myData.num_long_feed}</b>
                <p>포스트</p>
              </li>
              <li>
                <b>{myData.num_short_feed}</b>
                <p>모멘트</p>
              </li>
              <li>
                <b>{myData.num_like}</b>
                <p>좋아요</p>
              </li>
              <li>
                <b>{myData.num_comment}</b>
                <p>댓글</p>
              </li>
            </ul>
          </section>
          <section className={style["info-list"]}>
            <ul className={style["post-list"]}>
              {["포스트", "모멘트", "좋아요", "댓글"].map((post, index) => (
                <li
                  key={index}
                  className={`${style.post} ${activeIndex === index ? style.active : ""}`}
                  onClick={() => handleClick(index)}
                >
                  <button>{post}</button>
                </li>
              ))}
            </ul>
          </section>
          {/* <Feed feed={}/> */}
        </div>
      </div>
    </div>
  );
}

export default MyPage;
