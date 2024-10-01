import { useEffect, useMemo, useRef, useState } from 'react';
import style from './../pages/FeedPage/FeedPage.module.css';
import Feed, { Comments } from './feed';
import { FeedContext, FeedDispatchContext } from './../pages/FeedPage/FeedPage.js'


export default function InfFeed() {

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    let [feedData, setFeedData] = useState([]);
    let [nextData, setNextData] = useState([]);
    // 'http://127.0.0.1:4000/new_contents'
    // 'http://nova-platform.kr/home/home_feed'

    function fetchData() {
        // setIsLoading(true);
        fetch('https://nova-platform.kr/home/home_feed', {
            credentials: 'include',
        })
            .then(response => response.json())
            .then(data => {
                setFeedData(data.body.feed);
                setNextData(data.body.key);
                setIsLoading(false);
            })
        // .finally(() => setIsLoading(false));
    };

    function fetchPlusData() {
        // setIsLoading(true);
        fetch(`https://nova-platform.kr/home/home_feed?key=${nextData}`, {
            credentials: 'include',
        })
            .then(response => response.json())
            .then(data => {
                setNextData(data.body.key);
                setFeedData((prevData) => {
                    const newData = [...prevData, ...data.body.feed];
                    return newData;
                });

                console.log("111", nextData);
                console.log("222", data.body);
                console.log('333', feedData);
                setIsLoading(false);
            })
        // .finally(() => setIsLoading(false));
    };

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                // fetchData();
                fetchPlusData();
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
    }, [isLoading, nextData]);

    useEffect(() => {
        fetchData();
        return (() => {
            setFeedData([]);
        })
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    // let [numStar, setNumStar] = useState([]);
    // let [numComment, setNumComment] = useState([]);
    // let [isClickedStar, setIsClickedStar] = useState(false);
    // let [isClickedComment, setIsClickedComment] = useState(false);

    

   


    return (
        <div className={style['scroll-area']}>
            {
                feedData.map((a, i) => {
                    // console.log(a);
                    // console.log('class', a.fclass);
                    return (
                        <>
                            <Feed key={i} className='' feed={a} func={true} feedData={feedData} setFeedData={setFeedData}></Feed>
                            {/* <Comments feed={a}></Comments> */}
                        </>
                    )
                })
            }
            {isLoading && <p>Loading...</p>}
            <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

        </div>
    )
}