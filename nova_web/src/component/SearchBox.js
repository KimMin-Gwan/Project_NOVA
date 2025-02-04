import { useNavigate } from "react-router-dom";
import search_icon from "./../img/home_search.svg";
import style from "./feed-list/FeedThumbnail.module.css";

export default function SearchBox({
  type,
  searchWord,
  onClickSearch,
  onChangeSearchWord,
  onKeyDown,
}) {
  let navigate = useNavigate();

  function onClickSearchBtn(e) {
    e.stopPropagation();
    if (type === "search" || onClickSearch) {
      onClickSearch();
    }
  }
  return (
    <div
      className={style["search-section"]}
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        {
          !type && navigate("/search");
        }
      }}
    >
      {type === "search" ? (
        <input
          className={style["search-box"]}
          value={searchWord}
          onKeyDown={onKeyDown}
          onChange={onChangeSearchWord}
          placeholder="보고 싶은 최애를 검색해보세요"
          type="text"
        ></input>
      ) : (
        <div className={style["search-box"]}>보고 싶은 최애를 검색해보세요</div>
      )}
      <button
        className={style["search-btn"]}
        onClick={(e) => {
          onClickSearchBtn(e);
        }}
      >
        <img src={search_icon}></img>
      </button>
    </div>
  );
}
