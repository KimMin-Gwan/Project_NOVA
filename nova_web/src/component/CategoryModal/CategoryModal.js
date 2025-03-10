import { useEffect, useState } from "react";
import Board from "../Board/Board";
import "./index.css";
import ModalRectangle from "./../../img/ModalRectangle.png";

export default function CategoryModal({
  SetIsOpen,
  onClickCategory,
  biasId,
  board,
  setBoard,
  isOpend,
}) {
  let [boardData, setBoardData] = useState([]);
  let [isLoading, setIsLoading] = useState(true);
  const [backgroundColor, setBackgroundColor] = useState("");

  async function fetchBoardData() {
    await fetch(
      `https://nova-platform.kr/nova_sub_system/try_get_community_side_box?bid=${biasId}`,
      {
        credentials: "include",
      }
    )
      .then((response) => response.json())
      .then((data) => {
        setBoardData(data.body);
        setIsLoading(false);
      });
  }
  useEffect(() => {
    if (!isOpend) {
      setBackgroundColor("transparent"); //닫혀있을 때는 배경색 없애기
    } else {
      setTimeout(() => {
        setBackgroundColor("rgba(0, 0, 0, 0.5)"); //일정시간 지난 후에 뒤에 배경색 주기
      }, 500);
    }
  }, [isOpend]);

  useEffect(() => {
    fetchBoardData();
  }, []);

  if (isLoading) {
    return <div>로딩 중...</div>;
  }

  const handleTransitionEnd = (e) => {
    if (!isOpend) {
      setBackgroundColor("transparent"); // 애니메이션 후 배경색을 투명으로 변경
    }
  };

  return (
    <div
      className={`CategoryModal ${isOpend ? "see" : ""}`}
      style={{ backgroundColor }}
      onClick={() => {
        onClickCategory();
      }}
      onTransitionEnd={handleTransitionEnd}
    >
      <div
        className={`modal-container ${isOpend ? "on" : ""}`}
        onClick={(e) => e.stopPropagation()}
      >
        <section className="top-section">
          <img src={ModalRectangle} alt="모달 사각형" />
          <div className="modal-title">주제 이름</div>
        </section>
        <Board
          SetIsOpen={SetIsOpen}
          boardData={boardData}
          board={board}
          setBoard={setBoard}
        />
      </div>
    </div>
  );
}
