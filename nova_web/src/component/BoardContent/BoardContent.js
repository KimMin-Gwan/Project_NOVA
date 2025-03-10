import { useState, useEffect } from "react";
import "./index.css";
import useBoardStore from "../../stores/BoardStore/useBoardStore";

export default function BoardContent({ SetIsOpen, boardData }) {
  const [selected, setSelected] = useState(null);
  const { setBoard } = useBoardStore();

  useEffect(() => {
    // 모달이 열릴 때 로컬 스토리지에서 선택된 인덱스 가져오기
    if (SetIsOpen) {
      const savedIndex = localStorage.getItem("selectedBoardIndex");
      setSelected(savedIndex ? parseInt(savedIndex, 10) : null);
    }
  }, [SetIsOpen]);

  function onClickBoard(i) {
    setBoard(boardData.boards[i]);
    setSelected(i);
    localStorage.setItem("selectedBoardIndex", i); // 선택된 인덱스를 로컬 스토리지에 저장
  }

  return (
    <ul className="Board_content">
      {boardData &&
        boardData.boards.map((data, i) => (
          <li key={data.id ? data.id : `board-${i}`}>
            {data}
            <input
              type="radio"
              name="content"
              value={i}
              checked={selected === i}
              onChange={() => onClickBoard(i)}
            />
          </li>
        ))}
    </ul>
  );
}
