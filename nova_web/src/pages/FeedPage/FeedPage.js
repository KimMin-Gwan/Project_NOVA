import style from './FeedPage.module.css';
import stylePlanet from './../PlanetPage/Planet.module.css';

import planet2 from './../../img/planet2.png';
import { useEffect, useRef, useState } from 'react';
import Feed, { InputFeed } from '../../component/feed';
import { useNavigate } from 'react-router-dom';

export default function FeedPage() {
    //피드 드래그
    const [isFeedDragging, setIsFeedDragging] = useState(false);
    const [startY, setStartY] = useState(0);
    const [currentFeedY, setCurrentFeedY] = useState(0);

    function handleFeedMouseDown(e) {
        setStartY(e.clientY);
        setIsFeedDragging(true);
    };

    function handleFeedMouseMove(e) {
        if (isFeedDragging) {
            const moveY = e.clientY - startY;
            setCurrentFeedY(moveY);

            if (moveY < -50) {
                setSlideFeed(true);
                setUpFeed(true);
                setShowNewFeed(true);
            } 
            // else {
            //     setSlideFeed(false);
            //     setUpFeed(false);
            //     setShowNewFeed(false);
            // }
        }
    };

    function handleFeedMouseUp() {
        setIsFeedDragging(false);
        if (currentFeedY < -50) {
            setCurrentFeedY(0);
            // setSlideFeed(true);
        } else {
            setCurrentFeedY(100);
        }
    };


    // 행성 드래그
    const [isDragging, setIsDragging] = useState(false);
    const [dragStartY, setDragStartY] = useState(null);
    const [dragDirection, setDragDirection] = useState(null);
    const [showFeed, setShowFeed] = useState(false);

    const [slideFeed, setSlideFeed] = useState(false);
    const [upFeed, setUpFeed] = useState(false);
    const [showNewFeed, setShowNewFeed] = useState(false);

    const inputFeedRef = useRef(null);

    const [scrollPos, setScrollPos] = useState(0);

    let navigate = useNavigate();

    const [offsetY, setOffsetY] = useState(0);
    const boxRef = useRef(null);

    function handleMouseDown(e) {
        setIsDragging(true);
        setDragStartY(e.clientY);  // 드래그 시작 Y 좌표 기록
    };

    function handleMouseMove(e) {
        if (isDragging && dragStartY !== null) {
            const currentY = e.clientY;
            if (currentY > dragStartY) {
                setDragDirection('down');
                boxRef.current.style.transform = 'translateY(50px)';
                inputFeedRef.current.style.opacity = 1;
            } else if (currentY < dragStartY) {
                setDragDirection('up');
                boxRef.current.style.transform = 'translateY(-50px)';
                inputFeedRef.current.style.opacity = 0;

            }
        }
    };

    function handleMouseUp() {
        setIsDragging(false);

        if (dragDirection === 'down') {
            setShowFeed(true);
            // showFeed.current = true;  // 아래로 드래그하면 피드 표시

        } else if (dragDirection === 'up') {
            setShowFeed(false);

            // showFeed.current = false;  // 위로 드래그하면 피드 숨기기
        }
        boxRef.current.style.transform = 'translateY(0)';

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
            <div className={stylePlanet['top_area']}>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>은하계 탐색</div>
            </div>
            <div ref={inputFeedRef} className={`${style.boxx} ${showFeed ? '' : style.hidden}`}>
                <InputFeed></InputFeed>
            </div>
            <div ref={boxRef} className={style.databox}>
                <div className={style['img-area']} >
                    <img src={planet2} alt="Planet"
                        className={style.moving}
                        onMouseDown={handleMouseDown}
                        onMouseMove={handleMouseMove}
                        onMouseUp={handleMouseUp}
                        onMouseLeave={handleMouseUp}  // 마우스가 영역을 벗어날 때도 처리
                        style={{ cursor: isDragging ? 'grabbing' : 'grab' }} />
                </div>

                <div className={style.area}>
                    {showNewFeed && <Feed className={`${style.feedbox3}`}></Feed>}
                    <div
                        onMouseDown={handleFeedMouseDown}
                        onMouseMove={handleFeedMouseMove}
                        onMouseUp={handleFeedMouseUp}>
                        <Feed className={`${style.feedbox1} ${upFeed ? style['up_animate'] : ''}`}></Feed>
                        <Feed className={`${style.feedbox2} ${slideFeed ? style.animate : ''}`}></Feed>
                    </div>

                </div>
                <button onClick={() => {
                    onClickBox()
                }}>클릭</button>
            </div>
        </div >
    );
}
