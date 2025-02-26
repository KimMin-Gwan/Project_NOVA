import { useEffect, useState } from "react";
import Board from "../Board/Board";
import "./index.css";
import ModalRectangle from "./../../img/ModalRectangle.png";

export default function CategoryModal({ SetIsOpen, onClickCategory, biasId, board, setBoard }) {
  let [boardData, setBoardData] = useState([]);
  let [isLoading, setIsLoading] = useState(true);

  async function fetchBoardData() {
    await fetch(`https://nova-platform.kr/nova_sub_system/try_get_community_side_box?bid=${biasId}`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        setBoardData(data.body);
        setIsLoading(false);
      });
  }

  useEffect(() => {
    fetchBoardData();
  }, []);

  if (isLoading) {
    return <div>로딩 중...</div>;
  }

  return (
    <div
      className="CategoryModal"
      onClick={() => {
        onClickCategory();
      }}
    >
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <section className="top-section">
          <img src={ModalRectangle} alt="모달 사각형" />
          <div className="modal-title">주제 이름</div>
        </section>
        <Board SetIsOpen={SetIsOpen} boardData={boardData} board={board} setBoard={setBoard} />
      </div>
    </div>
  );
}
