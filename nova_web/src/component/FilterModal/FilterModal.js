import style from "./FilterModal.module.css";
import "./FilterModal.css";

export default function FilterModal({ isFilterClicked, onClickFilterButton }) {
  return (
    <div className="wrapper-container" onClick={onClickFilterButton}>
      <div className="FilterModal">
        <div className="FilterModal_title">
          <h3>딱 맞는 피드를 추천해드려요!</h3>
          <p>보고 싶은 게시글만 보여질 수 있도록, 지금 바로 경험해보세요.</p>
        </div>

        <div className="FilterModal_kind">
          <div>게시글 종류</div>
          <div className="button_container">
            <button>긴 글</button>
            <button>짧은 글</button>
            <button>노바 펀딩 콘텐츠</button>
          </div>
        </div>

        <div className="FilterModal_kind">
          <div>최애 성별</div>
          <div className="button_container">
            <button>남성</button>
            <button>여성</button>
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
