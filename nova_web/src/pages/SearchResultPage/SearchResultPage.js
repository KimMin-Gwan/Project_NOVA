import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import SearchBox from "../../component/SearchBox";
import { useEffect, useState } from "react";
import back from "./../../img/backword.png";
import logo2 from "../../img/logo2.png";
import "./index.css";
import style from "./../MyPage/Mypage.module.css";
import axios from "axios";
import FeedList from "../FeedList/FeedList";
import Feed from "../../component/feed";

export default function SearchResultPage() {
  // let params = useParams();
  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  // let keyword = params.keyword;
  let navigate = useNavigate();
  let [isLoading, setIsLoading] = useState(true);
  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

  const [activeIndex, setActiveIndex] = useState(null);
  let [nextKey, setNextKey] = useState(-1);

  const handleClick = (index) => {
    setActiveIndex(index);
  };

  let [feedData, setFeedData] = useState([]);

  function fetchSearchKeyword() {
    axios
      .get(
        `https://nova-platform.kr/feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${nextKey}`,
        {
          withCredentials: true,
        }
      )
      .then((res) => {
        setFeedData(res.data.body.send_data);
        console.log(res.data);
        setIsLoading(false);
        setNextKey(res.data.body.key);
      });
  }
  useEffect(() => {
    fetchSearchKeyword();
    console.log(feedData);
  }, []);

  if (isLoading) {
    return <div>loading...</div>;
  }

  return (
    <div className="container">
      <header className="header">
        <div
          className="logo"
          onClick={() => {
            navigate("/");
          }}
        >
          <img src={logo2} alt="logo" className={`logo-st`}></img>
        </div>
      </header>
      <div className="top-bar">
        <div
          className="back"
          onClick={() => {
            navigate(-1);
          }}
        >
          <img src={back} />
        </div>
        <SearchBox type="search" />
      </div>
      <section className={style["info-list"]}>
        <ul className={style["post-list"]}>
          {["포스트", "모멘트", "좋아요", "댓글"].map((post, index) => (
            <li
              key={index}
              className={`${style.post} ${activeIndex === index ? style.active : ""}`}
              onClick={() => handleClick(index)}
            >
              <p>{post}</p>
            </li>
          ))}
        </ul>
      </section>
      {feedData.map((feed, i) => {
        return <Feed key={feed.feed.fid} feed={feed.feed} />;
      })}
    </div>
  );
}
