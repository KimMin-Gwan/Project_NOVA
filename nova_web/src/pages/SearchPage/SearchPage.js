import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/backword.png";
import logo2 from "../../img/logo2.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import useTagStore from "../../stores/TagStore/useTagStore";
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
    navigate(`/search_result/?keyword=${searchWord}`);
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

  function onClickSearch(history) {
    if (history) {
      navigate(`/search_result?keyword=${history}`);
    } else {
      navigate(`/search_result?keyword=${searchWord}`);
    }
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
            navigate("/");
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
      {/* <p onClick={onDeleteAllHistory}>X</p> */}

      <section className="search-category">
        <h3>최근 검색어</h3>
        <div className="search-tag-box">
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
        </div>
      </section>

      <section className="search-category">
        <h3>추천 검색어</h3>
        <div className="search-tag-box">
          <div className="search-box-wrapper">
            <button className="search-tag">하이</button>
            <button className="search-tag">하이</button>
          </div>
        </div>
      </section>

      <section className="search-category">
        <h3>실시간 트렌드</h3>

        <ul className="tag-list">
          {tagList.map((tag, i) => {
            return <li key={i}>{tag}</li>;
          })}
        </ul>
      </section>
    </div>
  );
}
