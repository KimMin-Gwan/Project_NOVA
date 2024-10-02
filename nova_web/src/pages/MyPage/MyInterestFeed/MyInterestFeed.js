import { useNavigate } from 'react-router-dom';
import style from './../Mypage.module.css';
import feedStyle from './../../FeedPage/FeedPage.module.css';
import { useEffect, useState, useRef } from 'react';
import Feed from '../../../component/feed';

export default function MyInterestFeed() {
    let navigate = useNavigate();

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    let [myLikeFeed, setMyLikeFeed] = useState([]);
    let [nextFeed, setNextFeed] = useState([]);

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                fetchMoreMyStarFeed();
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


    function fetchMyStarFeed() {
        fetch('https://nova-platform.kr/user_home/get_stared_feed', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log('stared', data);
                setMyLikeFeed(data.body.feeds);
                setNextFeed(data.body.fid);
                setIsLoading(false);
            })
    };

    function fetchMoreMyStarFeed() {
        if (nextFeed !== '') {
            fetch(`https://nova-platform.kr/user_home/get_stared_feed?fid=${nextFeed}`, {
                credentials: 'include'
            })
                .then(response => response.json())
                .then(data => {
                    setMyLikeFeed((prevFeed) => {
                        const newLikeFeed = [...prevFeed, ...data.body.feeds];
                        return newLikeFeed;
                    });
                    setNextFeed(data.body.fid);
                    setIsLoading(false);
                })
        }
    };

    useEffect(() => {
        fetchMyStarFeed();
        return (() => {
            setMyLikeFeed([]);
        })
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>나의 관심 피드</div>
            </div>
            <div className={style['scroll-area']}>
                {
                    myLikeFeed.map((likeFeed, i) => {
                        return (
                            <Feed key={likeFeed.fid} className='' feed={likeFeed} func={true} feedData={myLikeFeed} setFeedData={setMyLikeFeed}></Feed>
                        )
                    })
                }
                {isLoading && <p>Loading...</p>}
                <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

            </div>
        </div>
    )
}