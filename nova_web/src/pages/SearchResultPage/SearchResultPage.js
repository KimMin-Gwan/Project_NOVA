import { useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import SearchBox from "../../component/SearchBox";
import { useEffect, useRef, useState } from "react";
import back from "./../../img/backword.png";
import logo2 from "../../img/logo2.png";
import "./index.css";
import style from "./../MyPage/Mypage.module.css";
import axios from "axios";
import FeedList from "../FeedList/FeedList";
import Feed from "../../component/feed";

export default function SearchResultPage() {
  // let params = useParams();
  const target = useRef(null);

  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  // let keyword = params.keyword;
  let navigate = useNavigate();
  let location = useLocation();
  let [isLoading, setIsLoading] = useState(true);
  let [searchWord, setSearchWord] = useState("");
  let [searchHistory, setSearchHistory] = useState([]);
  function handleNavigate() {
    // if (!searchWord) {
    //   navigate("/");
    // } else {
    // navigate(`/feed_list/search_feed?keyword=${searchWord}`);
    const updateHistory = [...searchHistory, searchWord];
    setSearchHistory(updateHistory);
    localStorage.setItem("history", JSON.stringify(updateHistory));
    navigate(`/search_result?keyword=${searchWord}`);
    navigate(0);
    setSearchWord("");
    // }
  }

  function handleMovePage(e, page) {
    e.preventDefault();
    navigate(page);
  }

  const [activeIndex, setActiveIndex] = useState(null);
  let [nextKey, setNextKey] = useState(-1);

  const handleClick = (index) => {
    setActiveIndex(index);
  };

  useEffect(() => {
    let historyList = JSON.parse(localStorage.getItem("history")) || [];
    setSearchHistory(historyList);
  }, []);

  function onKeyDown(event) {
    if (event.key === "Enter") {
      handleNavigate();
    }
  }

  function onChangeSearchWord(e) {
    setSearchWord(e.target.value);
  }
  function onClickSearch(history) {
    if (history) {
      navigate(`/search_result?keyword=${history}`);
    } else if (searchWord) {
      navigate(`/search_result?keyword=${searchWord}`);
    } else {
      alert("검색어를 입력해주세요.");
    }
  }

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
        setFeedData((prev) => {
          return [...prev, ...res.data.body.send_data];
        });
        console.log(res.data);
        setIsLoading(false);
        setNextKey(res.data.body.key);
      });
  }
  useEffect(() => {
    fetchSearchKeyword();
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        if (isLoading) return;

        fetchSearchKeyword();
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
  }, [nextKey]);

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
            navigate("/search");
          }}
        >
          <img src={back} />
        </div>
        <SearchBox
          type="search"
          value={keyword}
          // value={searchWord}
          onClickSearch={onClickSearch}
          onChangeSearchWord={onChangeSearchWord}
          onKeyDown={onKeyDown}
        />
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
      <div ref={target} style={{ height: "1px" }}></div>
    </div>
  );
}
