import style from './FeedPage.module.css';
import planet2 from './../../img/planet2.png';
import { useRef, useState } from 'react';

export default function FeedPage() {
    const [isDragging, setIsDragging] = useState(false);
    const [dragStartY, setDragStartY] = useState(null);
    const [dragDirection, setDragDirection] = useState(null);
    const showFeed = useRef(false);

    function handleMouseDown(e) {
        setIsDragging(true);
        setDragStartY(e.clientY);  // 드래그 시작 Y 좌표 기록
    };

    function handleMouseMove(e) {
        if (isDragging && dragStartY !== null) {
            const currentY = e.clientY;
            if (currentY > dragStartY) {
                setDragDirection('down');
            } else if (currentY < dragStartY) {
                setDragDirection('up');
            }
        }
    };

    function handleMouseUp() {
        setIsDragging(false);

        if (dragDirection === 'down') {
            showFeed.current = true;  // 아래로 드래그하면 피드 표시
        } else if (dragDirection === 'up') {
            showFeed.current = false;  // 위로 드래그하면 피드 숨기기
        }

        // 상태 초기화
        setDragStartY(null);
        setDragDirection(null);
    };

    return (
        <div className={style.container}>
            <br />
            {showFeed.current && <div className={style.feed}>피드 표시 중...</div>}

            <div className={style['img-area']}>
                <img src={planet2} alt="Planet"
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                    onMouseLeave={handleMouseUp}  // 마우스가 영역을 벗어날 때도 처리
                    style={{ cursor: isDragging ? 'grabbing' : 'grab' }} />
            </div>
            <div className={style.area}>gkgkgk</div>
        </div >
    );
}
