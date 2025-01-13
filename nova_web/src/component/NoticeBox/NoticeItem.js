import { useEffect, useRef, useState } from "react";
import "./index.css";

export default function NoticeItem({ notice, isLoading }) {
  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");
  let [hasDragged, setHasDragged] = useState(false);

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
    setHasDragged(false);
  }

  function onMouseUp(e) {
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
      setHasDragged(true);
    }
  }

  if (isLoading) {
    <div>데이터를 로딩 중입니다.</div>;
  }

  return (
    <div
      ref={scrollRef}
      onMouseDown={onMouseDown}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      className="notice-container"
    >
      <div className="notice-wrapper">
        <div key={notice.nid} className="notice-box">
          <div className="notice-img">
            <img alt="img?" />
          </div>

          <div className="notice-content">
            <b>{notice.title}</b>
            <p>{notice.bname ? `${notice.bname}` : "전체 공지사항"}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
