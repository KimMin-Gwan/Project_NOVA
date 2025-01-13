import "./index.css";

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
              {data}
            </li>
          );
        })}
    </ul>
  );
}
