import Board from "../Board/Board";
import "./index.css";

export default function CategoryModal({ onClickCategory }) {
  return (
    <div
      className="CategoryModal"
      onClick={() => {
        onClickCategory();
      }}
    >
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <h2>000님의 팬들을 위한 게시판</h2>
        <Board />
      </div>
    </div>
  );
}
