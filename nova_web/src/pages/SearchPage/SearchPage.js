import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/search_back.png";
import logo2 from "../../img/logo2.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import useTagStore from "../../stores/TagStore/useTagStore";
import NavBar from "../../component/NavBar/NavBar";
import Header from "../../component/Header/Header";
export default function SearchPage() {
  let navigate = useNavigate();

  let { tagList, loading, error, fetchTagList } = useTagStore();

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
    setSearchWord("");
    // }
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

  function onDeleteHistoryItem(e, index) {
    e.stopPropagation();
    const updateList = searchHistory.filter((item, i) => i !== index);
    // searchList = JSON.parse(searchList);
    setSearchHistory(updateList);
    localStorage.setItem("history", JSON.stringify(updateList));
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

  function onClickList(word) {
    if (word) {
      navigate(`/search_result?keyword=${word}`);
    } else {
      alert("검색어를 입력해주세요.");
    }
  }

  if (loading) {
    return <div>loading...</div>;
  }
  return (
    <div className="container">
      <Header />
      <div className="top-bar">
        <div
          className="back"
          onClick={() => {
            navigate("/");
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
      {/* <p onClick={onDeleteAllHistory}>X</p> */}

      <section className="search-category">
        <h3>최근 검색어</h3>
        <div className="search-tag-box">
          <SearchItems
            searchHistory={searchHistory}
            onClickSearch={onClickSearch}
            onDeleteHistoryItem={onDeleteHistoryItem}
          />
        </div>
      </section>

      <section className="search-category">
        <h3>실시간 트렌드</h3>

        <ul className="tag-list">
          {tagList.map((tag, i) => {
            return (
              <li
                key={i}
                onClick={() => {
                  onClickList(tag);
                }}
              >
                {tag}
              </li>
            );
          })}
        </ul>
      </section>
      <NavBar />
    </div>
  );
}

function SearchItems({ searchHistory, onClickSearch, onDeleteHistoryItem }) {
  return (
    <div className="search-box-wrapper">
      {searchHistory.length > 0 &&
        searchHistory.map((history, i) => {
          return (
            <button
              key={i}
              className="search-tag searched-tag"
              onClick={(e) => {
                onClickSearch(history);
              }}
            >
              {history}
              <p
                className="delete-tag"
                onClick={(e) => {
                  onDeleteHistoryItem(e, i);
                }}
              >
                X
              </p>
            </button>
          );
        })}
    </div>
  );
}
