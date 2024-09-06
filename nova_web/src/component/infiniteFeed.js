import { useEffect, useRef, useState } from 'react';
import style from './../pages/FeedPage/FeedPage.module.css';

export default function InfFeed() {

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(false);

    let [testData, setTestData] = useState([]);

    function fetchData() {
        setIsLoading(true);
        fetch('http://127.0.0.1:4000/new_contents')
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
                        <div className={style.feed} key={i}>{i}</div>
                    )
                })
            }
            {isLoading && <p>Loading...</p>}
            <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

        </div>
    )
}