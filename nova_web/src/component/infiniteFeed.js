import { useEffect, useRef, useState } from 'react';
import style from './../pages/FeedPage/FeedPage.module.css';
import Feed from './feed';

export default function InfFeed() {

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    let [feedData, setFeedData] = useState([]);
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
                console.log(data.body.feed);
                console.log("1111", feedData);
                setIsLoading(false);
            })
        // .finally(() => setIsLoading(false));
    };

    // const fetchData = async () => {
    //     try {
    //         const response = await fetch('https://nova-platform.kr/home/home_feed', {
    //             credentials: 'include',
    //         });
    //         const data = await response.json();
    //         setFeedData(data.body.feed);
    //         console.log(feedData);
    //     }
    //     catch (error) {
    //         console.error('Error fetching data: ', error);
    //     }
    // };

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                fetchData();
                console.log('3333', feedData)
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
    }, [isLoading]);

    useEffect(() => {
        return (
            setFeedData([])
        )
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    console.log("2222", feedData);
    return (
        <div className={style['scroll-area']}>

            <Feed className='' feed={feedData} ></Feed>
            {/* {
                feedData.map((a, i) => {
                    console.log(a);
                    console.log('class', a.fclass);
                    return (
                        <Feed key={a.fid} className='' feed={a.fclass} ></Feed>
                    )
                })
            } */}
            {isLoading && <p>Loading...</p>}
            <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

        </div>
    )
}