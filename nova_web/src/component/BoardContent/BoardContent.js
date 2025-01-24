import "./index.css";
import chat from "../../img/chatLight.png";

export default function BoardContent({ boardData, setBoard }) {
  function onClickBoard(i) {
    setBoard(boardData.boards[i]);
  }
  return (
    <ul className="Board_content">
      {boardData &&
        boardData.boards.map((data, i) => {
          return (
            <li key={i} onClick={() => onClickBoard(i)}>
              <img src={chat} alt="차트" />
              {data}
            </li>
          );
        })}
    </ul>
  );
}
