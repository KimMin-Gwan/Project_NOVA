import SearchBox from "../../component/SearchBox";
import "./index.css";
import back from "./../../img/backword.png";
import logo2 from "../../img/logo2.png";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import getTagList from "../../services/getTagList";
import useTagStore from "../../stores/tagList/useTagStore";
export default function SearchPage() {
  let navigate = useNavigate();
  //   let [tagList, setTagList] = useState([]);

  let { tagList, loading, error, fetchData } = useTagStore();

  useEffect(() => {
    fetchData();
    // getTagList().then((data) => {
    //   setTagList(data.body.hashtags);
    // });
  }, []);

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
        <SearchBox className="search" />
      </div>

      <section className="search-category">
        <h3>최근 검색어</h3>
        <div className="search-tag-box">
          <button className="search-tag">전한길</button>
          <button className="search-tag">전한길</button>
        </div>
      </section>

      <section className="search-category">
        <h3>인기 검색어</h3>
        <div>버튼</div>
      </section>

      <section className="search-category">
        <h3>실시간 트렌드</h3>
        {tagList.map((tag, i) => {
          return <div key={i}>{tag}</div>;
        })}
      </section>
    </div>
  );
}
