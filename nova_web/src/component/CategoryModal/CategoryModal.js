import { useEffect, useState } from "react";
import Board from "../Board/Board";
import "./index.css";

export default function CategoryModal({ onClickCategory, biasId, setBoard }) {
  let [boardData, setBoardData] = useState([]);
  let [isLoading, setIsLoading] = useState(true);

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
        console.log(data);
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
        <div className="modal-title">{boardData.bname}님의 팬들을 위한 게시판</div>
        <Board boardData={boardData} setBoard={setBoard} />
      </div>
    </div>
  );
}
