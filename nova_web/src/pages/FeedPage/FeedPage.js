import style from './FeedPage.module.css';
import planet2 from './../../img/planet2.png';
import { useRef, useState } from 'react';
import Feed, { InputFeed } from '../../component/feed';

export default function FeedPage() {
    const [isDragging, setIsDragging] = useState(false);
    const [dragStartY, setDragStartY] = useState(null);
    const [dragDirection, setDragDirection] = useState(null);
    const showFeed = useRef(false);

    const [slideFeed , setSlideFeed] = useState(false);

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


    function onClickBox(){
        setSlideFeed(!slideFeed);
    }

    return (
        <div className={style.container}>
            <br />
            {showFeed.current && <InputFeed></InputFeed>}

            <div className={style['img-area']}>
                <img src={planet2} alt="Planet"
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                    onMouseLeave={handleMouseUp}  // 마우스가 영역을 벗어날 때도 처리
                    style={{ cursor: isDragging ? 'grabbing' : 'grab' }} />
            </div>
            {/* <div className={style.containers}>
                <div className={style.box1}></div>
                <div className={style.box2}></div>
            </div> */}
            <div className={style.area}>
                <button onClick={()=>{
                    onClickBox()
                }}>클릭</button>
                <div className={`${style.feed} ${style.feedbox1}`}></div>
                <div className={`${style.feed} ${style.feedbox2} ${slideFeed ? style.animate : ''}`}></div>
            </div>
        </div >
    );
}
