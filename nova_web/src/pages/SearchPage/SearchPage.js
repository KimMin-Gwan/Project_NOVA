import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/search_back.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import NavBar from "../../component/NavBar/NavBar";
import Header from "../../component/Header/Header";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";
import style from "./SearchPageDesktop.module.css";
import SearchBoxDesktop from "../../component/SearchBoxDesktop";
import AdComponent from "../../component/AdComponent/AdComponent";


export default function SearchPage() {
  const isMobile = useMediaQuery('(max-width:1100px)');
  let navigate = useNavigate();

  // let { tagList, loading, error, fetchTagList } = useTagStore();

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

  if(isMobile){
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
          <div classname="ad-banner-strip">

          </div>

          <div className="search-tag-box">
            <SearchItems
              searchHistory={searchHistory}
              onClickSearch={onClickSearch}
              onDeleteHistoryItem={onDeleteHistoryItem}
            />
          </div>

        </section>
        <AdComponent type={"image_50x32"}/>
        <NavBar />
      </div>
    );
  }else{
    return(
      <DesktopLayout>
        <div className={style["desktop_search_page_outer_frame"]}>
          <div className={style["desktop_search_page_inner_frame"]}>
            <span className={style["search_page_header"]}>
              무엇을 찾으시나요?
            </span>
            <SearchBoxDesktop
              type="search"
              searchWord={searchWord}
              onClickSearch={onClickSearch}
              onChangeSearchWord={onChangeSearchWord}
              onKeyDown={onKeyDown}
            />
            <AdComponent type={"link"}/>
          </div>
        </div>
      </DesktopLayout>
    );
  }

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
