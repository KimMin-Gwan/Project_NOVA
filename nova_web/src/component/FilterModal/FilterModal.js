import style from "./FilterModal.module.css";
import "./FilterModal.css";

export default function FilterModal({ isFilterClicked, onClickFilterButton }) {
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
          <div>게시글 종류</div>
          <div className="button_container">
            <button>공지사항</button>
            <button>자유 게시판</button>
            <button>팬아트</button>
            <button>유머 게시판</button>
            <button>전체</button>
          </div>
        </div>

        <div className="FilterModal_kind">
          <div>컨텐츠 종류</div>
          <div className="button_container">
            <button>모멘트</button>
            <button>포스트</button>
            <button>전체</button>
          </div>
        </div>

        <div className="FilterModal_buttons">
          <button className="close_button" onClick={onClickFilterButton}>
            닫기
          </button>
          <button className="apply_button">적용</button>
        </div>
      </div>
    </div>
  );
}
