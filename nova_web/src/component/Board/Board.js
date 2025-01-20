import BoardContent from "../BoardContent/BoardContent";
import BoardTitle from "../BoardTitle/BoardTitle";
import "./index.css";

export default function Board({ boardData, setBoard }) {
  function handleRequestURL(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }

  return (
    <div className="Board">
      <BoardTitle>게시판 목록</BoardTitle>
      <BoardContent boardData={boardData} setBoard={setBoard} />

      <BoardTitle>외부 링크</BoardTitle>
      {/* link box */}
      <div className="LinkBox_container">
        <div
          className="LinkBox"
          onClick={() => handleRequestURL(boardData.urls.Instagram)}
        >
          <div className="LinkBox_img">
            <img src={boardData.urls.Instagram} alt="img" />
          </div>
          인스타
        </div>

        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.Naver)}>
          <div className="LinkBox_img">
            <img src={boardData.urls.Naver} alt="img" />
          </div>
          네이버
        </div>

        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.TikTok)}>
          <div className="LinkBox_img">
            <img src={boardData.urls.TikTok} alt="img" />
          </div>
          틱톡
        </div>

        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.X)}>
          <div className="LinkBox_img">
            <img src={boardData.urls.X} alt="img" />
          </div>
          X
        </div>
      </div>

      <BoardTitle>노바 펀딩</BoardTitle>
      <ul className="Board_content">
        <li>공식 판매 굿즈</li>
        <li>펀딩 상품</li>
      </ul>
    </div>
  );
}
