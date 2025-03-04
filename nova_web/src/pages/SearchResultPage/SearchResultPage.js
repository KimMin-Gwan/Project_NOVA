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

export default function SearchResultPage() {
  let [searchParams] = useSearchParams();
  let keyword = searchParams.get("keyword");
  let navigate = useNavigate();
  const target = useRef(null);

  let [searchWord, setSearchWord] = useState(keyword);
  let [searchHistory, setSearchHistory] = useState([]);

  let [feedData, setFeedData] = useState([]);
  const [comments, setComments] = useState([]);

  const [activeIndex, setActiveIndex] = useState(0);
  const [type, setType] = useState("post");

  const [feedNextKey, setFeedNextKey] = useState(-1);
  const [commentNextKey, setCommentNextKey] = useState(-1);

  let [isLoading, setIsLoading] = useState(true);

  function handleNavigate() {
    const updateHistory = [...searchHistory, searchWord];
    setSearchHistory(updateHistory);
    localStorage.setItem("history", JSON.stringify(updateHistory));
    navigate(`/search_result?keyword=${searchWord}`);
    navigate(0);
    setSearchWord("");
  }

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
      .get(`feed_explore/search_feed_with_keyword?keyword=${keyword}&key=${feedNextKey}`)
      .then((res) => {
        setFeedData((prev) => {
          return [...prev, ...res.data.body.send_data];
        });
        //console.log(res.data);
        setIsLoading(false);
        setFeedNextKey(res.data.body.key);
      });
  }

  async function fetchCommentKeyword() {
    await mainApi
      .get(`feed_explore/search_comment_with_keyword?keyword=${keyword}&key=${commentNextKey}`)
      .then((res) => {
        setComments(res.data.body.feeds);
        setIsLoading(false);
        setCommentNextKey(res.data.body.key);
      });
  }

  useEffect(() => {
    if (type === "post") {
      fetchSearchKeyword();
    } else if (type === "comment") {
      fetchCommentKeyword();
    }
  }, [type]);

  const onClickType = (data) => {
    setType(data === "게시글" ? "post" : "comment");
  };

  useEffect(() => {
    setFeedNextKey(-1);
    setCommentNextKey(-1);
    setFeedData([]);
  }, [type]);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        if (isLoading) return;

        if (type === "post") {
          fetchSearchKeyword();
        } else if (type === "comment") {
          fetchCommentKeyword();
        }
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
  }, [feedNextKey]);

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
      <Tabs activeIndex={activeIndex} handleClick={handleClick} onClickType={onClickType} />
      {type === "comment" && <Comments comments={comments} />}
      {type === "post" && <FeedSection feedData={feedData} />}

      <div ref={target} style={{ height: "1px" }}></div>
      <NavBar />
    </div>
  );
}
