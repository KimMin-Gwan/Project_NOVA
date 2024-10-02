import { useNavigate } from 'react-router-dom';
import style from './../Mypage.module.css';
import feedStyle from './../../FeedPage/FeedPage.module.css';
import { useEffect, useState, useRef } from 'react';
import Feed from '../../../component/feed';

export default function MyCommentFeed() {

    let navigate = useNavigate();

    const target = useRef(null);
    const observerRef = useRef(null);
    let [isLoading, setIsLoading] = useState(true);

    let [myComments, setMyComments] = useState([]);
    let [nextFeed, setNextFeed] = useState([]);

    useEffect(() => {
        observerRef.current = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                if (isLoading) return;

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

    function fetchMyComments() {
        fetch('https://nova-platform.kr/user_home/get_my_comments', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log('stared', data);
                setMyComments(data.body.comments);
                setNextFeed(data.body.cid);
                setIsLoading(false);
            })
    };

    useEffect(() => {
        fetchMyComments();
    }, []);

    if (isLoading) {
        return <p>데이터 </p>;
    }

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>나의 댓글 피드</div>
            </div>
            <div className={style['scroll-area']}>
                {
                    myComments.map((a, i) => {
                        // console.log(a);
                        // console.log('class', a.fclass);
                        return (
                            <>
                                {
                                    myComments.length === 0 ? <div>loading</div> :
                                    (
                                        <>
                                        <div>{a.cid}</div>
                                        <div>{a.body}</div>
                                        <div>{a.uname}</div>
                                        </>
                                    )
                                }
                                {/* <Comments feed={a}></Comments> */}
                            </>
                        )
                    })
                }
                {isLoading && <p>Loading...</p>}
                <div ref={target} style={{ height: "10px", backgroundColor: 'blue' }}></div>

            </div>
        </div>
    )
}