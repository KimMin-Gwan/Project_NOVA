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
        <div className="back">
          <img src={back} />
        </div>
        <SearchBox type="search" onClickSearch={onClickSearch} />
      </div>

      <section className="search-category">
        <h3>최근 검색어</h3>
        <div className="search-tag-box">
          <button className="search-tag">전한길</button>
        </div>
      </section>

      <section className="search-category">
        <h3>추천 검색어</h3>
        <div className="search-tag-box">
          {/* <div className="search-tag">버튼</div>
          <div className="search-tag">버튼</div>
          <div className="search-tag">버튼</div> */}
          <button className="search-tag">전한길</button>
          <button className="search-tag">전한길</button>
          <button className="search-tag">전한길</button>
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
