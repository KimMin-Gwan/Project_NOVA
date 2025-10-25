import "./FilterModal.css";
import { useEffect, useState } from "react";

let FilterData = [
  {
    id: 0,
    value: "공지사항",
    name: "공지사항",
  },
  {
    id: 1,
    value: "자유 게시판",
    name: "자유 게시판",
  },
  {
    id: 2,
    value: "팬아트",
    name: "팬아트",
  },
  {
    id: 3,
    value: "유머 후기 게시판",
    name: "유머 후기 게시판",
  },
  {
    id: 4,
    value: "",
    name: "전체",
  },
];


export default function FilterModal({
  onClickFilterButton,
  setFilterCategory,
  setFilterFclass,
  fetchAllFeed,
  onClickApplyButton1,
}) {
  let [filterBoard, setFilterBoard] = useState(JSON.parse(localStorage.getItem("board")) || [""]);

  let [isClickedFilterContent, setIsClickedFilterContent] = useState(
    JSON.parse(localStorage.getItem("content")) || ""
  );

  useEffect(() => {
    localStorage.setItem("board", JSON.stringify(filterBoard));
    localStorage.setItem("content", JSON.stringify(isClickedFilterContent));
  }, [filterBoard, isClickedFilterContent]);

  function onClickFilterBoard(name, value, i) {
    setFilterBoard((prev) => {
      if (prev.includes(value)) {
        return prev.filter((item) => item !== value);
      }
      return value === "" ? [value] : [...prev.filter((item) => item !== ""), value];
    });
    setFilterCategory((prev) => {
      const data = FilterData[i].value;
      if (prev.includes(data)) {
        return prev.filter((item) => item !== data);
      }
      return i === 4 ? [data] : [...prev.filter((item) => item !== FilterData[4].value), data];
    });
  }


  function onClickApplyButton2() {
    onClickApplyButton1();
    fetchAllFeed(true);
    onClickFilterButton();
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
          <p>보고 싶은 후기글만 보여질 수 있도록, 지금 바로 경험해보세요.</p>
        </div>

        <div className="FilterModal_kind">
          <h5>
            후기글 종류 <span>(중복선택 가능)</span>
          </h5>
          <div className="button_container">
            {FilterData.map((data, i) => {
              return (
                <button
                  className={`${filterBoard.includes(data.value) ? "clicked_button" : ""}`}
                  key={data.id}
                  onClick={() => onClickFilterBoard(data.name, data.value, i)}
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
            onClick={() => {
              onClickApplyButton2();
            }}
          >
            적용
          </button>
        </div>
      </div>
    </div>
  );
}
