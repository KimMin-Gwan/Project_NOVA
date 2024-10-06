import { useNavigate } from 'react-router-dom';
import style from './../Mypage.module.css';
import feedStyle from './../../FeedPage/FeedPage.module.css';
import { useEffect, useState, useRef } from 'react';
import Feed from '../../../component/feed';

export default function MyActiveFeed() {
    let navigate = useNavigate();

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    let [myActiveFeed, setMyActiveFeed] = useState([]);
    let [nextFeed, setNextFeed] = useState([]);

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                fetchMoreMyActiveFeed();
            });
        });

        if (target.current) {
            observerRef.current.observe(target.current);
        }

        return () => {
            if (observerRef.current && target.current) {
                observerRef.current.unobserve(target.current);
            }
        };
    }, [isLoading, nextFeed]);


    function fetchMyActiveFeed() {
        fetch('https://nova-platform.kr/user_home/get_interactied_feed', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log('inter', data);
                setMyActiveFeed(data.body.feeds);
                setNextFeed(data.body.fid);
                setIsLoading(false);
            })
    };

    function fetchMoreMyActiveFeed() {
        if (nextFeed !== '') {
            fetch(`https://nova-platform.kr/user_home/get_interactied_feed?fid=${nextFeed}`, {
                credentials: 'include'
            })
                .then(response => response.json())
                .then(data => {
                    console.log('stared2222', data);
                    setMyActiveFeed((prevFeed) => {
                        const newActFeed = [...prevFeed, ...data.body.feeds];
                        return newActFeed;
                    });
                    setNextFeed(data.body.fid);
                    setIsLoading(false);
                })
        }
    };

    useEffect(() => {
        fetchMyActiveFeed();
        return (() => {
            setMyActiveFeed([]);
        })
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>은하계 탐색</div>
            </div>
            <div className={style['scroll-area']}>
                {
                    myActiveFeed.map((actFeed, i) => {
                        return (
                            <Feed key={actFeed.fid} className='' feed={actFeed} func={true} feedData={myActiveFeed} setFeedData={setMyActiveFeed}></Feed>
                        )
                    })
                }
                {isLoading && <p>Loading...</p>}
                <div ref={target} className={style['observe_line']}></div>

            </div>
        </div>
    )
}