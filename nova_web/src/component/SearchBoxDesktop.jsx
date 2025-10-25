import { useNavigate } from "react-router-dom";
import search_icon from "./../img/home_search.svg";
import style from "./SearchBoxDesktop.module.css";

export default function SearchBoxDesktop({
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
    <div className={style["search_input_wrapper"]}>
        <input className={style["search_input"]}
        value={searchWord}
        onKeyDown={onKeyDown}
        onChange={(e) => {
            onChangeSearchWord(e);
        }}
        placeholder="콘텐츠 또는 후기를 검색 할 수 있어요"
        type="text"
        />
    </div>
  );
}
