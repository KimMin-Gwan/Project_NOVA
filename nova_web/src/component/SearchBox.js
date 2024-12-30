import search_icon from "./../img/search_icon.png";
import style from "./feed-list/FeedThumbnail.module.css";

export default function SearchBox() {
  return (
    <div className={style["search-section"]}>
      <input
        id="search-box"
        className={style["search-box"]}
        type="text"
        placeholder="보고 싶은 최애를 검색해보세요"
      ></input>
      <button className={style["search-btn"]}>
        <img src={search_icon}></img>
      </button>
    </div>
  );
}
