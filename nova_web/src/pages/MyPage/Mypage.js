import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import style from "./Mypage.module.css";
import mypage_more_icon from "./../../img/mypage_more.png";
import user_icon from "./../../img/user.svg";
import mainApi from "../../services/apis/mainApi";
import Feed from "../../component/feed";

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
  { category: "댓글" },
];
function MyPage() {
  let navigate = useNavigate();

  let [isLoading, setIsLoading] = useState(true);
  let [myData, setMyData] = useState();
  let [myFeed, setMyFeed] = useState([]);
  const [nextKey, setNextKey] = useState(-1);

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
      console.log("feeed", res.data);
      setMyFeed(res.data.body.feed);
      setNextKey(res.data.body.key);
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

  const [activeIndex, setActiveIndex] = useState(0);

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
            src={`https://kr.object.ncloudstorage.com/nova-user-profile/${myData?.uid}.png`}
            alt="img"
          />
        </div>
        <div>
          <section className={style["user-name"]}>
            <h3>{myData.uname}</h3>
            <img
              src={mypage_more_icon}
              alt=""
              onClick={(e) => handleMovePage(e, "/mypage_edit")}
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
            <ul className={style["post-list"]} data-active-index={activeIndex}>
              {categoryData.map((item, index) => (
                <li
                  key={index}
                  className={`${style.post} ${activeIndex === index ? style.active : ""}`}
                  onClick={() => {
                    fetchMyFeed(item.type);
                    handleClick(index);
                  }}
                >
                  <button>{item.category}</button>
                </li>
              ))}
            </ul>
          </section>

          {myFeed.map((feed, i) => {
            return <Feed key={i} feed={feed} />;
          })}
        </div>
      </div>
    </div>
  );
}

export default MyPage;
