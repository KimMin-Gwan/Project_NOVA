import style from "./FilterModal.module.css";
import "./FilterModal.css";
import { useState } from "react";

export default function FilterModal({
  isFilterClicked,
  onClickFilterButton,
  setFilterCategory,
  setFilterFclass,
  fetchAllFeed,
  onClickApplyButton1,
  setNextData,
}) {
  let FilterData = [
    {
      id: 0,
      value: "공지사항",
      name: "공지사항",
    },
    {
      id: 1,
      value: "자유게시판",
      name: "자유게시판",
    },
    {
      id: 2,
      value: "팬아트",
      name: "팬아트",
    },
    {
      id: 3,
      value: "유머게시판",
      name: "유머게시판",
    },
    {
      id: 4,
      value: "",
      name: "전체",
    },
  ];

  let ContentData = [
    { id: 0, value: "short", name: "모멘트" },
    { id: 1, value: "long", name: "포스트" },
    { id: 2, value: "", name: "전체" },
  ];

  let boolData = [true, false]

  let [isClickedFilterBoard, setIsClickedFilterBoard] = useState([]);
  let [isClickedFilterContent, setIsClickedFilterContent] = useState(0);

  function onClickFilterBoard(i) {
    setIsClickedFilterBoard((prev) => {
      // return i === 4 ? [i] : [...prev, i];

      if (prev.includes(i)) {
        return prev.filter((item) => item !== i);
      }
      return i === 4 ? [i] : [...prev.filter((item) => item !== 4), i];
    });
    console.log(isClickedFilterBoard);
    setFilterCategory((prev) => {
      const data = FilterData[i].value;

      if (prev.includes(data)) {
        return prev.filter((item) => item !== i);
      }
      return i === 4
        ? [data]
        : [...prev.filter((item) => item !== FilterData[4].value), data];
    });
  }
  function onClickFilterContent(i) {
    setIsClickedFilterContent(i);
    setFilterFclass(ContentData[i].value);
  }

  function onClickApplyButton2() {
    onClickApplyButton1()
    fetchAllFeed(true);
  }


  return (
    <div className="wrapper-container" onClick={onClickFilterButton}>
      <div
        className="FilterModal"
        onClick={(e) => {
          e.stopPropagation();
        }}
      >
        <div className="FilterModal_title">
          <h3>딱 맞는 피드를 추천해드려요!</h3>
          <p>보고 싶은 게시글만 보여질 수 있도록, 지금 바로 경험해보세요.</p>
        </div>

        <div className="FilterModal_kind">
          <h5>게시글 종류</h5>
          <div className="button_container">
            {FilterData.map((data, i) => {
              return (
                <button
                  className={`${
                    isClickedFilterBoard.includes(i) ? "clicked_button" : ""
                  }`}
                  key={data.id}
                  onClick={() => onClickFilterBoard(i)}
                >
                  {data.name}
                </button>
              );
            })}
          </div>
        </div>

        <div className="FilterModal_kind">
          <h5>컨텐츠 종류</h5>
          <div className="button_container">
            {ContentData.map((data, i) => {
              return (
                <button
                  className={isClickedFilterContent === i ? "clicked_button" : ""}
                  key={data.id}
                  onClick={() => onClickFilterContent(i)}
                >
                  {data.name}
                </button>
              );
            })}
          </div>
        </div>

        <div className="FilterModal_buttons">
          <button className="close_button" onClick={onClickFilterButton}>
            닫기
          </button>
          <button
            className="apply_button"
            onClick={() => { onClickApplyButton2()}}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
}
