import Feed, { InputFeed, InfoArea, Text, Comments } from '../../component/feed';

import style from './../FeedPage/FeedPage.module.css';
import stylePlanet from './../PlanetPage/Planet.module.css';
import { CiStar } from "react-icons/ci";
import { TfiCommentAlt } from "react-icons/tfi";
import { PiShareFatLight } from "react-icons/pi";
import { MdOutlineReportProblem } from "react-icons/md";

import React, { useState, useEffect, useRef } from 'react';
// import style from './../pages/FeedPage/FeedPage.module.css';
import { useLocation, useNavigate } from 'react-router-dom';

const WriteFeed = () => {

    // const location = useLocation();

    // const queryParams = new URLSearchParams(location.search);
    // const fclass = queryParams.get('fclass');

    // const [banners, setBanners] = useState([]);
    // const [nextData, setNextData] = useState(0);
    // const [currentIndex, setCurrentIndex] = useState(0);
    // const [isDragging, setIsDragging] = useState(false);
    // const [startY, setStartY] = useState(0);
    // const [translateY, setTranslateY] = useState(0);
    // const [dragDistance, setDragDistance] = useState(0);
    // const sliderRef = useRef(null);



    // useEffect(() => {
    //     setTranslateY(-currentIndex * window.innerHeight);
    // }, [currentIndex]);

    // const handleMouseDown = (e) => {
    //     setIsDragging(true);
    //     setStartY(e.clientY);
    // };

    // const handleMouseMove = (e) => {
    //     if (!isDragging) return;

    //     const distance = e.clientY - startY;
    //     setDragDistance(distance);
    //     // setIsClickedComment(false);
    //     setTranslateY(-currentIndex * window.innerHeight + distance);
    // };

    // const handleMouseUp = () => {
    //     setIsDragging(false);

    //     const threshold = 100;
    //     if (dragDistance > threshold && currentIndex > 0) {
    //         setCurrentIndex(currentIndex - 1);
    //         setIsClickedComment(false);
    //     } else if (dragDistance < -threshold && currentIndex < banners.length - 1) {
    //         setCurrentIndex(currentIndex + 1);
    //         setIsClickedComment(false);
    //     }

    //     setDragDistance(0);
    // };

    // // 휠로 배너 변경
    // const handleWheel = (e) => {
    //     if (e.deltaY > 0 && currentIndex < banners.length - 1) {
    //         setCurrentIndex((prevIndex) => prevIndex + 1);
    //         setIsClickedComment(false);
    //     } else if (e.deltaY < 0 && currentIndex > 0) {
    //         setCurrentIndex((prevIndex) => prevIndex - 1);
    //         setIsClickedComment(false);
    //     }
    // };

    // function fetchFeed() {
    //     fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=${fclass}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log("11", data.body.feed);
    //             setBanners(data.body.feed);
    //             setNextData(data.body.key);
    //             // setNumStar([data.body.feed[0].star, data.body.feed[1].star]);
    //             // setNumComment([data.body.feed[0].num_comment, data.body.feed[1].num_comment])
    //         })
    // }

    // useEffect(() => {
    //     fetchFeed();
    // }, [])

    // // 서버에서 추가 데이터를 받아오는 함수
    // const fetchMoreBanners = async () => {
    //     try {
    //         // 서버로부터 추가 배너 데이터를 가져옴
    //         const response = await fetch(`https://nova-platform.kr/feed_explore/get_feed?fclass=${fclass}&key=${nextData}`); // 예시 URL
    //         const newBanners = await response.json();
    //         const plusFeed = newBanners.body.feed;
    //         // const newStar = newBanners.body.feed[0].star;
    //         // const comments = newBanners.body.feed[0].num_comment;
    //         setNextData(newBanners.body.key);
    //         // 기존 배너에 새 배너를 추가
    //         setBanners((prevBanners) => [...prevBanners, ...plusFeed]);
    //         // setNumStar((prevNumStar) => [...prevNumStar, newStar]);
    //         // setNumComment((prevNumComment) => [...prevNumComment, comments])
    //     } catch (error) {
    //         console.error('Error fetching additional banners:', error);
    //     }
    // };

    // // currentIndex가 마지막 배너일 때 추가 배너를 불러옴
    // useEffect(() => {
    //     if (currentIndex === banners.length - 1) {
    //         fetchMoreBanners();

    //     }
    // }, [currentIndex]);


    let navigate = useNavigate();

    // let [numStar, setNumStar] = useState([]);
    // let [numComment, setNumComment] = useState([]);
    // // let [isClickedStar, setIsClickedStar] = useState(false);
    // let [isClickedComment, setIsClickedComment] = useState(false);

    // function handleCheckStar(fid, index) {
    //     // setIsClickedStar(!isClickedStar);
    //     fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
    //         credentials: 'include',
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             setBanners((prevBanners) => {
    //                 return prevBanners.map((banner) => {
    //                     return banner.fid === fid ? { ...banner, star: data.body.feed[0].star } : banner
    //                 })
    //             })
    //         })
    // };

    // function handleShowCommentWindow() {
    //     setIsClickedComment(!isClickedComment);
    // };

    // let header = {
    //     "request-type": "default",
    //     "client-version": 'v1.0.1',
    //     "client-ip": '127.0.0.1',
    //     "uid": '1234-abcd-5678',
    //     "endpoint": "/core_system/",
    // }

    // let [inputValue, setInputValue] = useState('');

    // function handleChange(e) {
    //     setInputValue(e.target.value);
    // };


    // let [newComments, setNewComments] = useState([]);

    // function handleSubmit(fid, event) {
    //     event.preventDefault();

    //     fetch('https://nova-platform.kr/feed_explore/make_comment', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             header,
    //         },
    //         credentials: 'include',
    //         body: JSON.stringify({
    //             header: header,
    //             body: {
    //                 fid: `${fid}`,
    //                 body: `${inputValue}`
    //             }
    //         })
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log(data);
    //             // setNewComments(data.body.comments);
    //             setAllComments((prevAllComments)=>{
    //                 const newAllComments = [data.body.comments[0], ...prevAllComments];
    //                 return newAllComments;
    //             })
    //             setBanners((prevBanners) => {
    //                 return prevBanners.map((banner) => {
    //                     return banner.fid === fid ? { ...banner, num_comment: data.body.feed[0].num_comment } : banner
    //                 })
    //             })
    //             setInputValue('');
    //         })
    // }

    // let [allComments, setAllComments] = useState([]);
    // let [commentCount, setCommentCount] = useState(0);
    // let [isClickedCommentWindow, setIsClickedCommentWindow] = useState(false);

    // function handleShowComment(fid,event) {
    //     event.preventDefault();
    //     fetch(`https://nova-platform.kr/feed_explore/view_comment?fid=${fid}`, {
    //         credentials: 'include'
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log("show",data.body);
    //             setAllComments(data.body.comments);

    //         })
    // };

    // useEffect(()=>{
    //     console.log("pleae",allComments);
    //     // handleShowComment();
    // },[allComments]);

    // let [isClickedLikeBtn, setIsClickedLikeBtn] = useState(false);
    // let [commentLikes, setCommentLikes] = useState(0);
    // function handleCommentLike(fid, cid, event){
    //     event.preventDefault();
    //     fetch(`https://nova-platform.kr/feed_explore/like_comment?fid=${fid}&cid=${cid}`,
    //         {
    //             credentials: 'include'
    //         })
    //         .then(response=>response.json())
    //         .then(data=>{
    //             console.log('like', data.body.comments);

    //             setAllComments((prevAll)=>{
    //                 return prevAll.map((comment,i) => {
    //                     return comment.cid === cid ? { ...comment, like: data.body.comments[i].like } : comment
    //                 })
    //                 const newAllComments = [...prevAll]
    //             })
    //             console.log("244241242414",allComments);
    //             setCommentLikes(data.body.comments);
    //         })
    // }

    // let [isClickedRemoveBtn, setIsClickedRemoveBtn] = useState(false);
    // function handleRemoveComment(fid, cid, event){
    //     event.preventDefault();

    //     const newAll = allComments.filter((comment)=>comment.cid!==cid);
    //     setAllComments(newAll);


    //     fetch(`https://nova-platform.kr/feed_explore/remove_comment?fid=${fid}&cid=${cid}`,
    //         {
    //             credentials: 'include'
    //         })
    //         .then(response=>response.json())
    //         .then(data=>{
    //             console.log('remove',data.body.comments);
    //             // setAllComments((prevAll)=>{
    //             //     const newAllComments = [data.body.comments];
    //             //     return newAllComments;
    //             // })
    //         })
    // };


    return (
        <div className={style['test_container']}>
            <div className={`${stylePlanet['top_area']} ${style['top_bar_area']}`}>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>글쓰기</div>
            </div>

            <div style={{ height: '50px' }}></div>
            <div className={style.test} >
                <div className={style['short_form_container']}>
                    <div className={style['short_box']}>
                        <div className={style['img_circle']}></div>
                        <div style={{ height: '80px' }}></div>
                        <div className={style['short_feed']}>
                            <div className={style['write_container']}>
                                <div className={style['text_body']}>
                                    <textarea placeholder='내용을 입력해주세요' className={style['write_body']}></textarea>
                                </div>

                                <div className={style['contents_area']}>
                                    {/* 넷중하나 */}
                                    {/* <div className={style['one_of_four_area']}>
                                        <ol className={style['one_of_four_list']}>
                                            <li>
                                                1. <input></input>
                                            </li>
                                            <li>
                                                2. <input></input>
                                            </li>
                                            <li>
                                                3. <input></input>
                                            </li>
                                            <li>
                                                4. <input></input>
                                            </li>
                                        </ol>
                                    </div> */}
                                    {/* 둘 중 하나 */}
                                    {/* <div>
                                        <div className={`${style['button_container']}`}>
                                            <input maxLength={10} className={`${style['select_button']} ${style['balance_btn']}`}></input>
                                            <input className={`${style['select_button']} ${style['balance_btn']}`}></input>
                                        </div>
                                    </div> */}
                                    {/* 정거장 */}
                                    <div className={style['station_container']}>
                                        <div className={style['station_box']}>
                                            <input type='text' className={style['site_name']} placeholder='사이트 이름'></input>
                                            <input type='text' className={style['site_script']} placeholder='설명'></input>
                                            <input type='url' className={style['site_url']} placeholder='url'></input>
                                        </div>
                                    </div>
                                </div>

                                <div className={style['func_part']}>
                                    <div className={style['btn_func_area']}>
                                        <div className={style['btn_func']}>
                                            <label>
                                                <input type='checkbox'></input>댓글 허용
                                            </label>
                                            <label>
                                                <input type='checkbox'></input>공유 허용
                                            </label>
                                        </div>
                                        <button>업로드</button>
                                    </div>
                                    <div className={style['warning_text']}>타인에게 불편을 줄 수 있는 내용의 게시글은 경고 없이 삭제될 수 있습니다.</div>
                                </div>

                            </div>


                        </div>
                        {/* <Feed className={style['short_feed']}></Feed> */}
                        {/* <div className={style['comment_action']}>
                            <form onSubmit={(event) => handleSubmit(banner.fid, event)}>
                                <input type='text' value={inputValue} onChange={handleChange}></input>
                                <button type='submit'>댓글 작성</button>
                            </form>
                        </div> */}
                        {/* </div> */}

                    </div>

                    {/* <div className={style['function_button']}> */}
                    {/* <div className={style['func_btn']}>
                            <button onClick={() => {
                                handleCheckStar(banner.fid, i);
                            }}>
                                <CiStar className={style['func_btn_img']} />
                            </button>
                            <p>{numStar[i]}</p>
                            <p>{banner.star}</p>

                        </div> */}
                    {/* <div className={style['func_btn']}>
                            <button onClick={(event) => {
                                handleShowComment(banner.fid, event);
                                handleShowCommentWindow();
                                // handleCheckComment(banner.fid, i);
                            }}>
                                <TfiCommentAlt className={style['func_btn_img']} />
                            </button>
                            <p>{banner.num_comment}</p>
                        </div>
                        <div className={style['func_btn']}>
                            <button>
                                <PiShareFatLight className={style['func_btn_img']} />
                            </button>
                            <p>공유</p>
                        </div>
                        <div className={style['func_btn']}>
                            <button>
                                <MdOutlineReportProblem className={style['func_btn_img']} />
                            </button>
                            <p>신고</p>
                        </div> */}
                    {/* </div> */}

                </div>

            </div>

        </div>


    );
};

export default WriteFeed;