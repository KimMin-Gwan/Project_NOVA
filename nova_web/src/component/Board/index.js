import BoardContent from "../BoardContent";
import BoardTitle from "../BoardTitle";
import "./index.css";

export default function Board() {
  {
    /* board */
  }
  return (
    <div className="Board">
      <BoardTitle>게시판 목록</BoardTitle>
      <BoardContent />

      <BoardTitle>외부 링크</BoardTitle>
      {/* link box */}
      <div className="LinkBox_container">
        <div className="LinkBox">
          <div className="LinkBox_img">
            <img alt="img" />
          </div>
          방송국
        </div>
      </div>

      <BoardTitle>노바 펀딩</BoardTitle>
      <BoardContent />
    </div>
  );
}
