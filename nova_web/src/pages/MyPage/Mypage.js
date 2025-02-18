import { useNavigate } from "react-router-dom";
import React, { useEffect, useRef, useState } from "react";
import style from "./Mypage.module.css";
import mypage_more_icon from "./../../img/mypage_more.png";
import user_icon from "./../../img/user_profile.svg";
import mainApi from "../../services/apis/mainApi";
import Feed from "../../component/feed";
import arrow from "./../../img/comment_arrow.svg";
import reArrow from "./../../img/recomment.svg";

const categoryData = [
  {
    type: "post",
    category: "포스트",
  },
  {
    type: "moment",
    category: "모멘트",
  },
  {
    type: "like",
    category: "좋아요",
  },
  {
    type: "comment",
    category: "댓글",
  },
];
function MyPage() {
  const target = useRef(null);
  const observerRef = useRef(null);
  let navigate = useNavigate();

  let [isLoading, setIsLoading] = useState(true);
  let [myData, setMyData] = useState();
  let [myFeed, setMyFeed] = useState([]);
  const [nextKey, setNextKey] = useState(-1);
  const [nowCategory, setNowCategory] = useState(categoryData[0].type);
  const [isComment, setIsComment] = useState(false);
  async function fetchMyPage() {
    await mainApi.get("user_home/get_my_page_data").then((res) => {
      console.log("my", res.data);
      setMyData(res.data.body);
      setIsLoading(false);
    });
  }

  useEffect(() => {
    fetchMyPage();
  }, []);

  async function fetchMyFeed(category) {
    await mainApi.get(`user_home/get_my_feed?type=${category}&key=${nextKey}`).then((res) => {
      console.log("feed", res.data);
      setMyFeed((prevData) => [...prevData, ...res.data.body.feed]);
      setNextKey(res.data.body.key);
      setIsLoading(false);
    });
  }

  useEffect(() => {
    fetchMyFeed(nowCategory);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        if (isLoading) return;

        fetchMyFeed(nowCategory);
      });
    });

    if (target.current) {
      observer.observe(target.current);
    }

    return () => {
      if (target.current) {
        observer.unobserve(target.current);
      }
    };
  }, [nowCategory, nextKey]);

  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    setMyFeed([]);
    setNextKey(-1);
  }, [nowCategory]);

  const handleClick = (index, type) => {
    setNextKey(-1);
    setActiveIndex(index);
  };

  const [isClickedComment, setIsClickedComment] = useState(false);

  function onClickComment() {
    setIsClickedComment(!isClickedComment);
  }

  if (isLoading) {
    return <div>loading...</div>;
  }

  function handleComment() {
    setIsComment(!isComment);
  }
  const profile = `https://kr.object.ncloudstorage.com/nova-user-profile/${myData.uid}.png`;

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
          <img src={profile} alt="img" onError={(e) => (e.target.src = user_icon)} />
        </div>
        <div className={style["feed-wrapper"]}>
          <section className={style["user-name"]}>
            <h3>{myData.uname}</h3>
            <img src={mypage_more_icon} alt="" onClick={(e) => handleMovePage(e, "/mypage_edit")} style={{ cursor: "pointer" }} />
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
                <p onClick={onClickComment}>댓글</p>
              </li>
            </ul>
          </section>
          <section className={style["info-list"]}>
            <ul className={style["post-list"]} data-active-index={activeIndex}>
              {categoryData.map((item, index) => (
                <li
                  key={index}
                  className={`${style.post} ${activeIndex === index ? style.active : ""}`}
                  onClick={() => {
                    setNowCategory(item.type);
                    handleClick(index, item.type);
                    console.log(item.type);
                  }}
                >
                  <button>{item.category}</button>
                </li>
              ))}
            </ul>
          </section>

          {isClickedComment && (
            <div className={style["MyPage_Comment_Box"]}>
              <div className={style["Feed_title"]} onClick={handleComment}>
                <img src={arrow} alt="화살표" />
                <p>이 예시문은 어쩌구 저쩌구</p>
              </div>

              {isComment && (
                <section className={style["comment_box"]}>
                  <img src={reArrow} alt="대댓글" />
                  <p className={style["Comment_content"]}>댓글내용</p>
                  <span>2025-02-05</span>
                </section>
              )}
            </div>
          )}
          {myFeed.map((feed, i) => {
            return <Feed key={i} feed={feed} />;
          })}
          <div ref={target} style={{ height: "1px" }}></div>
        </div>
      </div>
    </div>
  );
}

export default MyPage;
