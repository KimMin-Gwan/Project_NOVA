import { useEffect, useRef, useState } from 'react';
import style from './../pages/FeedPage/FeedPage.module.css';
import Feed from './feed';

export default function InfFeed() {

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(false);

    let [testData, setTestData] = useState([]);
    // 'http://127.0.0.1:4000/new_contents'
    // 'http://nova-platform.kr/home/home_feed'
    function fetchData() {
        setIsLoading(true);
        fetch('http://127.0.0.1:4000/home/home_feed', {
            credentials: 'include',
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setTestData(prevData => [...prevData, ...data]);
            })
            .finally(() => setIsLoading(false));
    };

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                fetchData();
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
            setTestData([])
        )
    }, []);

    return (
        <div className={style['scroll-area']}>
            {
                testData.map((a, i) => {
                    return (
                        <Feed key={i} type={a} className=''></Feed>
                    )
                })
            }
            {isLoading && <p>Loading...</p>}
            <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

        </div>
    )
}