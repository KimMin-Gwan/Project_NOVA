import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate, useNavigation, useParams } from "react-router-dom";
import style from "./WriteFeed.module.css";
import useBiasStore from "../../stores/BiasStore/useBiasStore.js";

const categoryData = [
  { key: 0, category: "자유게시판" },
  { key: 1, category: "팬아트" },
  { key: 2, category: "유머게시판" },
];

const WriteMoment = () => {
  let { biasList, loading, fetchBiasList } = useBiasStore();
  const navigate = useNavigate();
  let [biasId, setBiasId] = useState();

  return (
    <div className={style["nav_moment"]}>
      <form>
        <section className={style["Select_container"]}>
          <div className={style["section_title"]}>주제 선택</div>
          <DropDownSection options={biasList} setBiasId={setBiasId} />
          <div
            className={style["more-find"]}
            onClick={() => {
              navigate("/follow_page");
            }}
          >
            더 많은 주제 찾아보기
          </div>
        </section>

        <section className={style["Select_container"]}>
          <div className={style["section_title"]}>카테고리 선택</div>
          <DropDownSection options={categoryData} />
        </section>
      </form>
    </div>
  );
};

export default WriteMoment;

function DropDownSection({ options, setBiasId }) {
  const [showTopic, setShowTopic] = useState(false);
  const [currentTopic, setCurrentTopic] = useState("선택 없음");
  function onClickTopic() {
    setShowTopic(!showTopic);
  }

  function onClickSelectTopic(e, bid) {
    // console.log(e.target.innerText);
    setCurrentTopic(e.target.innerText);
    setShowTopic(!showTopic);
    if (setBiasId) {
      setBiasId(bid);
    }
  }
  return (
    <>
      <label className={style["Select_box"]} onClick={onClickTopic}>
        {currentTopic}
      </label>
      <ul className={`${showTopic ? style["Select_options_on"] : style["Select_options"]}`}>
        <li onClick={onClickSelectTopic}>선택 없음</li>
        {options &&
          options.map((option, i) => {
            return (
              <li
                key={option.bid || option.key}
                value={option.bname || option.category}
                onClick={(e) => {
                  onClickSelectTopic(e, option.bname);
                }}
              >
                {option.bname || option.category}
              </li>
            );
          })}
      </ul>
    </>
  );
}
