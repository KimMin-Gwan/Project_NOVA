import React, { useState } from 'react';
import './DraggableBox.css'; // CSS 파일을 연결

const Box = () => {
  const [isDragged, setIsDragged] = useState(false);
  const [startY, setStartY] = useState(0);
  const [currentY, setCurrentY] = useState(0);

  const handleMouseDown = (e) => {
    setStartY(e.clientY);
    setIsDragged(true);
  };

  const handleMouseMove = (e) => {
    if (isDragged) {
      const moveY = e.clientY - startY;
      setCurrentY(moveY);
    }
  };

  const handleMouseUp = () => {
    setIsDragged(false);
    if (currentY < -50) { // 일정 거리 이상 위로 드래그 되었을 때
      setCurrentY(0); // 상단에 고정 (애니메이션 실행)
    } else {
      setCurrentY(100); // 원래 위치로 돌아감
    }
  };

  return (
    <div
      className={`box11 ${currentY === 0 ? 'up' : ''}`} 
      style={{ transform: `translateY(${currentY}px)` }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      <div className="content">
        글 제목
        <br />
        글 내용
      </div>
      <div className="icon">⬆️</div>
    </div>
  );
};

export default Box;
