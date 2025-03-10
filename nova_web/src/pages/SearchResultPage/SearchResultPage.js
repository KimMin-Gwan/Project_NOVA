import { useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/search_back.png";
import NavBar from "../../component/NavBar/NavBar";
import mainApi from "../../services/apis/mainApi";
import Header from "../../component/Header/Header";
import Comments from "../../component/Comments/Comments";
import Tabs from "../../component/Tabs/Tabs";
import FeedSection from "../../component/FeedSection/FeedSection";
import useIntersectionObserver from "../../hooks/useIntersectionObserver";

export default function SearchResultPage() {
  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  let navigate = useNavigate();

  // 검색어 상태
  let [searchWord, setSearchWord] = useState(keyword);
  let [searchHistory, setSearchHistory] = useState([]);

  // 탭 및 데이터 타입 상태
  const [activeIndex, setActiveIndex] = useState(0);
  const [type, setType] = useState("post");

  // 데이터 관련 상태
  let [feedData, setFeedData] = useState([]);
  const [comments, setComments] = useState([]);
  let [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);

  // 페이지네이션 키
  const [feedNextKey, setFeedNextKey] = useState(-1);
  const [commentNextKey, setCommentNextKey] = useState(-1);

  useEffect(() => {
    let historyList = JSON.parse(localStorage.getItem("history")) || [];
    setSearchHistory(historyList);
  }, []);

  useEffect(() => {
    setIsLoading(true);
  }, [activeIndex]);

  useEffect(() => {
    setFeedNextKey(-1);
    setCommentNextKey(-1);
    setFeedData([]);
    setComments([]);

    if (type === "post") {
      fetchSearchKeyword();
    } else if (type === "comment") {
      fetchCommentKeyword();
    }
  }, [type]);

  async function fetchSearchKeyword() {
    await mainApi
      .get(`feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${feedNextKey}`)
      .then((res) => {
        setFeedData((prev) => {
          return [...prev, ...res.data.body.send_data];
        });
        setHasMore(res.data.body.send_data.length > 0);
        setFeedNextKey(res.data.body.key);
        setIsLoading(false);
      });
  }

  async function fetchCommentKeyword() {
    await mainApi
      .get(`feed_explore/search_comment_with_keyword?keyword=${keyword}&key=${commentNextKey}`)
      .then((res) => {
        setComments((prev) => [...prev, ...res.data.body.feeds]);
        setHasMore(res.data.body.feeds.length > 0);
        setIsLoading(false);
        setCommentNextKey(res.data.body.key);
      });
  }

  function loadMoreCallBack() {
    if (!hasMore || isLoading) return;

    if (type === "post") {
      fetchSearchKeyword();
    } else if (type === "comment") {
      fetchCommentKeyword();
    }
  }

  const targetRef = useIntersectionObserver(loadMoreCallBack, { threshold: 0.5 }, hasMore);

  function handleNavigate() {
    const updateHistory = [...searchHistory, searchWord];
    setSearchHistory(updateHistory);
    localStorage.setItem("history", JSON.stringify(updateHistory));
    navigate(`/search_result?keyword=${searchWord}`);
    navigate(0);
    setSearchWord("");
  }

  function handleSearchWord(e) {
    setSearchWord(e.target.value);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter") {
      handleNavigate();
    }
  }

  const handleClick = (index) => {
    setActiveIndex(index);
  };

  function handleSearch(history) {
    if (history) {
      navigate(`/search_result?keyword=${history}`);
    } else if (searchWord) {
      navigate(`/search_result?keyword=${searchWord}`);
    } else {
      alert("검색어를 입력해주세요.");
    }
  }

  const onClickType = (data) => {
    setType(data === "게시글" ? "post" : "comment");
  };

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
          onClickSearch={handleSearch}
          onChangeSearchWord={handleSearchWord}
          onKeyDown={handleKeyDown}
        />
      </div>
      <Tabs activeIndex={activeIndex} handleClick={handleClick} onClickType={onClickType} />
      {type === "comment" && <Comments comments={comments} isLoading={isLoading} />}
      {type === "post" && (
        <FeedSection feedData={feedData} setFeedData={setFeedData} isLoading={isLoading} />
      )}

      <div ref={targetRef} style={{ height: "1px" }}></div>
      <NavBar />
    </div>
  );
}
