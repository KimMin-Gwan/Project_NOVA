import { useNavigate } from 'react-router-dom';
import style from './../Mypage.module.css';
import feedStyle from './../../FeedPage/FeedPage.module.css';
import { useEffect, useState, useRef } from 'react';
import Feed from '../../../component/feed';

export default function MyWriteFeed() {

    let navigate = useNavigate();

    let [myFeed, setMyFeed] = useState([]);
    let [nextFeed, setNextFeed] = useState([]);

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    function fetchMyFeed() {
        fetch('https://nova-platform.kr/user_home/get_my_feed', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log('feed', data);
                setMyFeed(data.body.feeds);
                setNextFeed(data.body.fid);
                setIsLoading(false);
            })
    };

    function fetchMoreMyFeed() {
        // setIsLoading(true);
        if (nextFeed !== '') {
            fetch(`https://nova-platform.kr/user_home/get_my_feed?fid=${nextFeed}`, {
                credentials: 'include',
            })
                .then(response => response.json())
                .then(data => {
                    setNextFeed(data.body.fid);
                    setMyFeed((prevData) => {
                        const newData = [...prevData, ...data.body.feeds];
                        return newData;
                    });

                    // console.log("111", nextData);
                    console.log("222", data.body);
                    // console.log('333', feedData);
                    setIsLoading(false);
                })
        }
        // .finally(() => setIsLoading(false));
    };

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                fetchMoreMyFeed();
                // fetchData();
                // fetchPlusData();
                // fetchMoreMyStarFeed();
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



    useEffect(() => {
        fetchMyFeed();
        return (() => {
            setMyFeed([]);
        })
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>나의 작성 피드</div>
            </div>
            <div className={style['scroll-area']}>
                {
                    myFeed.map((writeFeed, i) => {
                        return (
                            <Feed key={writeFeed.fid} className='' feed={writeFeed} func={true} feedData={myFeed} setFeedData={setMyFeed}></Feed>
                        )
                    })
                }
                {isLoading && <p>Loading...</p>}
                <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

            </div>
        </div>
    )
}