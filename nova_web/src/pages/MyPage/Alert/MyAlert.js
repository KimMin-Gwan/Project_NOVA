import { useNavigate } from 'react-router-dom';
import style from './../Mypage.module.css';
import feedStyle from './../../FeedPage/FeedPage.module.css';
import { useEffect, useState, useRef } from 'react';
import Feed from '../../../component/feed';

export default function MyAlert() {

    let navigate = useNavigate();

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    let [myAlerts, setMyAlerts] = useState([]);
    let [nextAlert, setNextAlert] = useState([]);

    function fetchMyAlerts() {
        fetch('https://nova-platform.kr/user_home/get_my_alert', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log('alalalerts', data);
                setMyAlerts(data.body.alert);
                setNextAlert(data.body.aid);
                setIsLoading(false);
            })
    };

    // function fetchMoreMyAlerts() {
    //     if (nextAlert !== -1) {
    //         fetch(`https://nova-platform.kr/user_home/get_my_alert?aid=${nextAlert}`, {
    //             credentials: 'include'
    //         })
    //             .then(response => response.json())
    //             .then(data => {
    //                 console.log(data);
    //                 setMyAlerts((prevAlerts) => {
    //                     const newAlerts = [...prevAlerts, ...data.body.alert];
    //                 });
    //                 setNextAlert(data.body.aid);
    //                 setIsLoading(false);
    //             })
    //     }
    // };

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

                // fetchMoreMyAlerts();
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
    }, [isLoading, nextAlert]);



    useEffect(() => {
        fetchMyAlerts();
        // return (() => {
        //     setMyAlerts([]);
        // })
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>나의 알림</div>
            </div>
            <div className={style['scroll-area']}>
                {
                    myAlerts.map((a, i) => {
                        return (
                            <>
                                {
                                    myAlerts.length === 0 ? <div>loading</div> :
                                        (
                                            <>
                                                <div>{a.aid}</div>
                                                {/* <div>{a.cid}</div>
                                                <div>{a.body}</div>
                                                <div>{a.uname}</div> */}
                                            </>
                                        )
                                }
                                {/* <Comments feed={a}></Comments> */}
                            </>
                        )
                    })
                }
                {isLoading && <p>Loading...</p>}
                <div ref={target} className={style['observe_line']}></div>

            </div>
        </div>
    )
}