import BoardContent from "../BoardContent/BoardContent";
import BoardTitle from "../BoardTitle/BoardTitle";
import youtube from "../../img/youtube.svg";
import naver from "../../img/naver.svg";
import chzzz from "../../img/chzzz.svg";
import "./index.css";

export default function Board({ SetIsOpen, boardData }) {
  const linkItem = [
    {
      id: 0,
      name: "네이버",
      src: naver,
      url: boardData.urls.Naver,
    },
    {
      id: 1,
      name: "유튜브",
      src: youtube,
      url: boardData.urls.TikTok,
    },
    {
      id: 2,
      name: "방송국",
      src: chzzz,
      url: boardData.urls.TikTok,
    },
  ];

  return (
    <div className="Board">
      <BoardTitle>게시판 목록</BoardTitle>
      <BoardContent SetIsOpen={SetIsOpen} boardData={boardData} />
      <BoardTitle>외부 링크</BoardTitle>
      <BoardLink linkItem={linkItem} />
    </div>
  );
}

function BoardLink({ linkItem }) {
  function handleRequestURL(url) {
    window.open(url, "_blank", "noopener, noreferrer");
  }
  return (
    <div className="LinkBox_container">
      {linkItem.map((item) => {
        return (
          <div key={item.id} className="LinkBox" onClick={() => handleRequestURL(item.url)}>
            <div className="LinkBox_img">
              <img src={item.src} alt="img" />
            </div>
            <div>{item.name}</div>
          </div>
        );
      })}
    </div>
  );
}
