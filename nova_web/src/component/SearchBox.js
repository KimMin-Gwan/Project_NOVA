import { useNavigate } from "react-router-dom";
import search_icon from "./../img/search_icon.png";
import style from "./feed-list/FeedThumbnail.module.css";

export default function SearchBox() {
  let navigate = useNavigate();
  return (
    <div
      className={style["search-section"]}
      onClick={() => {
        navigate("/search");
      }}
    >
      <div className={style["search-box"]}>인기 게시글 검색</div>
      <button className={style["search-btn"]}>
        <img src={search_icon}></img>
      </button>
    </div>
  );
}
