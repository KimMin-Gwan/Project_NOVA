import style from './FeedPage.module.css';
import planet2 from './../../img/planet2.png';
import { useEffect, useRef, useState } from 'react';
import Feed, { InputFeed } from '../../component/feed';

export default function FeedPage() {
    const [isDragging, setIsDragging] = useState(false);
    const [dragStartY, setDragStartY] = useState(null);
    const [dragDirection, setDragDirection] = useState(null);
    const [planetAnimate, setPlanetAnimate] = useState(false);
    const showFeed = useRef(false);

    const [slideFeed, setSlideFeed] = useState(false);
    const [upFeed, setUpFeed] = useState(false);
    const [showNewFeed, setShowNewFeed] = useState(false);


    useEffect(() => {
        const currentScroll = window.scrollY;
        // document.body.style.overflow = 'hidden';
        if (currentScroll < 500) {
            window.scrollTo(0,500);
        }

        return () => {
            document.body.style.overflow = '';
        }
    }, []);


    function handleMouseDown(e) {
        setIsDragging(true);
        setDragStartY(e.clientY);  // 드래그 시작 Y 좌표 기록
    };

    function handleMouseMove(e) {
        if (isDragging && dragStartY !== null) {
            const currentY = e.clientY;
            if (currentY > dragStartY) {
                setDragDirection('down');
                window.scrollTo(0,0);
                document.body.style.overflow = '';

            } else if (currentY < dragStartY) {
                setDragDirection('up');
                window.scrollTo(0,500);
                document.body.style.overflow = 'hidden';
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


    function onClickBox() {
        setSlideFeed(!slideFeed);
        setUpFeed(!upFeed);
        setShowNewFeed(!showNewFeed);
    }

    return (
        <div className={style.container}>
            <div className={style.boxx} style={{ overflowY: 'hidden' }}>
                <InputFeed></InputFeed>
            </div>
            <div style={{ overflowY: 'hidden' }}>
                <div className={style['img-area']}>
                    <img src={planet2} alt="Planet"
                        onMouseDown={handleMouseDown}
                        onMouseMove={handleMouseMove}
                        onMouseUp={handleMouseUp}
                        onMouseLeave={handleMouseUp}  // 마우스가 영역을 벗어날 때도 처리
                        style={{ cursor: isDragging ? 'grabbing' : 'grab' }} />
                </div>

                <div className={style.area}>
                    <button onClick={() => {
                        onClickBox()
                    }}>클릭</button>

                    {showNewFeed && <Feed className={`${style.feedbox3}`}></Feed>}
                    <Feed className={`${style.feedbox1} ${upFeed ? style['up_animate'] : ''}`}></Feed>
                    <Feed className={`${style.feedbox2} ${slideFeed ? style.animate : ''}`}></Feed>
                </div>
            </div>
        </div >
    );
}
