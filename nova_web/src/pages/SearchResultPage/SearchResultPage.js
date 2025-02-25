import { useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import SearchBox from "../../component/SearchBox";
import { useEffect, useRef, useState } from "react";
import back from "./../../img/search_back.png";
import logo2 from "../../img/logo2.png";
import "./index.css";
import style from "./../MyPage/Mypage.module.css";
import axios from "axios";
import Feed from "../../component/feed";
import NavBar from "../../component/NavBar";
import mainApi from "../../services/apis/mainApi";
import Header from "../../component/Header/Header";
import MyComments from "../../component/Comments/Comments";
import Comments from "../../component/Comments/Comments";

export default function SearchResultPage() {
  // let params = useParams();
  const target = useRef(null);

  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  // let keyword = params.keyword;
  let navigate = useNavigate();
  let location = useLocation();
  let [isLoading, setIsLoading] = useState(true);
  let [searchWord, setSearchWord] = useState(keyword);
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
  let [feedData, setFeedData] = useState([]);

  const [type, setType] = useState("post");

  const [activeIndex, setActiveIndex] = useState(0);
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

  async function fetchSearchKeyword() {
    await mainApi
      .get(`feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${nextKey}`)
      .then((res) => {
        setFeedData((prev) => {
          return [...prev, ...res.data.body.send_data];
        });
        console.log(res.data);
        setIsLoading(false);
        setNextKey(res.data.body.key);
      });
  }
  const [comments, setComments] = useState([]);

  async function fetchCommentKeyword() {
    console.log("댓글 불러짐");
    await mainApi
      .get(`feed_explore/search_comment_with_keyword?keyword=${keyword}&key=${nextKey}`)
      .then((res) => {
        // setFeedData((prev) => {
        //   return [...prev, ...res.data.body.send_data];
        // });
        console.log("댓글", res.data);
        setComments(res.data.body.feeds);
        // setIsLoading(false);
        // setNextKey(res.data.body.key);
      });
  }

  useEffect(() => {
    if (type === "post") {
      fetchSearchKeyword();
    } else if (type === "comment") {
      fetchCommentKeyword();
    }
  }, [type]);

  useEffect(() => {
    setFeedData([]);
    setNextKey(-1);
  }, [type]);

  const onClickType = (data) => {
    if (data === "게시글") {
      setType("post");
    } else if (data === "댓글") {
      setType("comment");
    }
  };

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
    <div className="container search_result_page">
      <Header />
      <div className="top-bar ">
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
          searchWord={searchWord}
          onClickSearch={onClickSearch}
          onChangeSearchWord={onChangeSearchWord}
          onKeyDown={onKeyDown}
        />
      </div>
      <section className={`${style["info-list"]} ${style["search-nav-bar"]}`}>
        <ul className={style["post-list"]} data-active-index={activeIndex}>
          {["게시글", "댓글"].map((post, index) => (
            <li
              key={index}
              className={`${style.post} ${activeIndex === index ? style.active : ""}`}
              onClick={() => {
                handleClick(index);
                onClickType(post);
              }}
            >
              <p>{post}</p>
            </li>
          ))}
        </ul>
      </section>
      {type === "comment" && <Comments comments={comments} />}

      {type === "post" && (
        <section className="feed_section">
          {feedData.map((feed, i) => {
            return <Feed key={feed.feed.fid} feed={feed.feed} />;
          })}
        </section>
      )}
      <div ref={target} style={{ height: "1px" }}></div>
      <NavBar />
    </div>
  );
}
