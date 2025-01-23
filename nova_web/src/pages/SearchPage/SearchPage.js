import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/backword.png";
import logo2 from "../../img/logo2.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import getTagList from "../../services/getTagList";
import useTagStore from "../../stores/tagList/useTagStore";
import axios from "axios";
export default function SearchPage() {
  let navigate = useNavigate();
  //   let [tagList, setTagList] = useState([]);

  let { tagList, loading, error, fetchTagList } = useTagStore();

  let [searchWord, setSearchWord] = useState("");
  let [searchHistory, setSearchHistory] = useState([]);

  function handleNavigate() {
    if (!searchWord) {
      navigate("/");
    } else {
      // navigate(`/feed_list/search_feed?keyword=${searchWord}`);
      const updateHistory = [...searchHistory, searchWord];
      setSearchHistory(updateHistory);
      localStorage.setItem("history", JSON.stringify(updateHistory));
      setSearchWord("");
    }
  }

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

  function onDeleteAllHistory() {
    localStorage.removeItem("history");
    setSearchHistory([]);
  }

  function onDeleteHistoryItem(index) {
    const updateList = searchHistory.filter((item, i) => i !== index);
    // searchList = JSON.parse(searchList);
    setSearchHistory(updateList);
    localStorage.setItem("history", JSON.stringify(updateList));
  }

  useEffect(() => {
    fetchTagList();
    // getTagList().then((data) => {
    //   setTagList(data.body.hashtags);
    // });
  }, []);

  // function fetchRecommendKeyword() {
  //   fetch("https://nova-platform.kr/home_search/get_recommend_keyword", {
  //     credentials: "include",
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log(data);
  //     });
  //   // axios
  //   //   .get("https://nova-platform.kr/home_search/get_recommend_keyword", {
  //   //     withCredentials: true,
  //   //   })
  //   //   .then((res) => console.log(res.data));
  // }

  // useEffect(() => {
  //   fetchRecommendKeyword();
  // }, []);

  function onClickSearch() {
    navigate("/search_result");
  }

  if (loading) {
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
        <SearchBox
          type="search"
          value={searchWord}
          onClickSearch={onClickSearch}
          onChangeSearchWord={onChangeSearchWord}
          onKeyDown={onKeyDown}
        />
      </div>

      <section className="search-category">
        <h3>최근 검색어</h3>
        <div className="search-tag-box">
          {/* <p onClick={onDeleteAllHistory}>X</p> */}

          {searchHistory.length > 0 &&
            searchHistory.map((history, i) => {
              return (
                <>
                  <button key={i} className="search-tag">
                    {history}
                  </button>
                  <p
                    onClick={() => {
                      onDeleteHistoryItem(i);
                    }}
                  >
                    X
                  </p>
                </>
              );
            })}
        </div>
      </section>

      <section className="search-category">
        <h3>추천 검색어</h3>
        <div className="search-tag-box">
          {/* <div className="search-tag">버튼</div>
          <div className="search-tag">버튼</div>
          <div className="search-tag">버튼</div> */}
          <button className="search-tag">채현찌</button>
        </div>
        {/* <button className="search-tag">전한길</button> */}
      </section>

      <section className="search-category">
        <h3>실시간 트렌드</h3>
        <ul className="tag-list">
          {tagList.map((tag, i) => {
            return (
              <li key={i}>
                {i + 1} {tag}
              </li>
            );
          })}
        </ul>
      </section>
    </div>
  );
}
