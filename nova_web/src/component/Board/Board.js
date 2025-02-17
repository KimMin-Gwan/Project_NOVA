import BoardContent from "../BoardContent/BoardContent";
import BoardTitle from "../BoardTitle/BoardTitle";
import "./index.css";
import chat from "../../img/chatLight.png";
import ticket from "../../img/Ticket_light.png";
import insta from "../../img/insta_color.png";
import youtube from "../../img/youtube.svg";
import naver from "../../img/naver.svg";
import chzzz from "../../img/chzzz.svg";
import x_img from "../../img/x_color.png";

export default function Board({ SetIsOpen, boardData, setBoard }) {
  function handleRequestURL(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }

  return (
    <div className="Board">
      <BoardTitle>게시판 목록</BoardTitle>
      <BoardContent SetIsOpen={SetIsOpen} boardData={boardData} setBoard={setBoard} />

      <BoardTitle>외부 링크</BoardTitle>
      {/* link box */}
      <div className="LinkBox_container">
        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.Instagram)}>
          <div className="LinkBox_img">
            <img src={insta} alt="img" />
          </div>
          인스타
        </div>

        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.Naver)}>
          <div className="LinkBox_img">
            <img src={naver} alt="img" />
          </div>
          네이버
        </div>

        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.TikTok)}>
          <div className="LinkBox_img">
            <img src={boardData.urls.TikTok} alt="img" />
          </div>
          틱톡
        </div>
        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.TikTok)}>
          <div className="LinkBox_img">
            <img src={youtube} alt="img" />
          </div>
          유튜브
        </div>
        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.TikTok)}>
          <div className="LinkBox_img">
            <img src={chzzz} alt="img" />
          </div>
          방송국
        </div>

        <div className="LinkBox" onClick={() => handleRequestURL(boardData.urls.X)}>
          <div className="LinkBox_img">
            <img src={x_img} alt="img" />
          </div>
          X
        </div>
      </div>

      {/* <BoardTitle>노바 펀딩</BoardTitle>
      <ul className="Board_content">
        <li>
          <img src={ticket} alt="" />
          공식 판매 굿즈
        </li>
        <li>
          <img src={ticket} alt="" />
          펀딩 상품
        </li>
      </ul> */}
    </div>
  );
}
