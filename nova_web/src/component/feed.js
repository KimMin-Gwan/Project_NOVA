import style from './../pages/FeedPage/FeedPage.module.css';
import planet1 from './../img/planet1.png';
import planet2 from './../img/planet2.png';
import planet3 from './../img/planet3.png';
import planet4 from './../img/planet4.png';
import { useState } from 'react';
// import {}
// import { useRef, useState } from 'react';

export default function Feed({ className, feed, func, feedData, setFeedData }) {

    function handleInteraction(event, fid, action) {
        event.preventDefault();

        fetch(`https://nova-platform.kr/feed_explore/interaction_feed?fid=${fid}&action=0`, {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
    }

    // 댓글 더보기 - 본문 보기
    let [isClickedMoreSee, setIsClickedMoreSee] = useState(false);

    function handleMoreSee() {
        setIsClickedMoreSee(!isClickedMoreSee);
    };


    function handleCheckStar(fid, e) {
        e.preventDefault();
        // setIsClickedStar(!isClickedStar);
        fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
            credentials: 'include',
        })
            .then(response => response.json())
            .then(data => {
                setFeedData((prevFeeds) => {
                    return prevFeeds.map((feed) => {
                        return feed.fid === fid ? { ...feed, star: data.body.feed[0].star } : feed
                    })
                })
            })
    };


    let [allComments, setAllComments] = useState([]);
    let [commentCount, setCommentCount] = useState(0);
    let [isClickedCommentWindow, setIsClickedCommentWindow] = useState(false);

    // 댓글 보기
    function handleShowComment(fid, event) {
        event.preventDefault();
        fetch(`https://nova-platform.kr/feed_explore/view_comment?fid=${fid}`, {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log("show", data.body);
                setAllComments(data.body.comments);
            })
    };

    let [isClickedLikeBtn, setIsClickedLikeBtn] = useState(false);
    let [commentLikes, setCommentLikes] = useState(0);

    // 댓글 좋아요 기능
    function handleCommentLike(fid, cid, event) {
        event.preventDefault();
        fetch(`https://nova-platform.kr/feed_explore/like_comment?fid=${fid}&cid=${cid}`,
            {
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                console.log('like', data.body.comments);

                setAllComments((prevAll) => {
                    return prevAll.map((comment, i) => {
                        return comment.cid === cid ? { ...comment, like: data.body.comments[i].like } : comment
                    })
                })
                setCommentLikes(data.body.comments);
            })
    }

    // 댓글 삭제 기능
    let [isClickedRemoveBtn, setIsClickedRemoveBtn] = useState(false);

    function handleRemoveComment(fid, cid, event) {
        event.preventDefault();

        const newAll = allComments.filter((comment) => comment.cid !== cid);
        setAllComments(newAll);


        fetch(`https://nova-platform.kr/feed_explore/remove_comment?fid=${fid}&cid=${cid}`,
            {
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                console.log('remove', data.body.comments);
                // setAllComments((prevAll)=>{
                //     const newAllComments = [data.body.comments];
                //     return newAllComments;
                // })
            })
    }

    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }

    return (

        <>
            {
                feed.fclass === 'card' &&
                (
                    <div className={`${style.feed} ${className}`} >
                        <div>
                            <InfoArea color={'#7960EC'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        <div className={style['comments_box']}>
                                            {
                                                allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                                    (
                                                        allComments.map((comment, i) => {
                                                            return (
                                                                <div key={comment.cid} className={style['comment']} on>
                                                                    <div>{i}</div>
                                                                    <div>{comment.uname}</div>
                                                                    <div>{comment.body}</div>
                                                                    <div onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>
                                                                    <div>신고</div>
                                                                    <div onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)}>{comment.like}</div>
                                                                </div>
                                                            )
                                                        })
                                                    )
                                            }
                                        </div>
                                    </div>) : <Text data={feed.body}></Text>
                            }
                        </div>
                        <div style={{ width: '100%', height: '50px' }}></div>
                        {
                            func && (
                                <div className={style['function_box']}>
                                    {
                                        isClickedMoreSee ? (<div onClick={handleMoreSee}>본문 보기</div>) : (
                                            <div onClick={(event) => {
                                                handleMoreSee();
                                                handleShowComment(feed.fid, event);
                                            }}>댓글 더보기</div>)
                                    }
                                    <div>신고</div>
                                    <div onClick={(e) => { handleCheckStar(feed.fid, e) }}>좋아요 {feed.star}</div>
                                </div>
                            )
                        }

                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData} ></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'multiple' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <div>
                            <InfoArea color={'#E370D1'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        <div className={style['comments_box']}>
                                            {
                                                allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                                    (
                                                        allComments.map((comment, i) => {
                                                            return (
                                                                <div key={comment.cid} className={style['comment']} on>
                                                                    <div>{i}</div>
                                                                    <div>{comment.uname}</div>
                                                                    <div>{comment.body}</div>
                                                                    <div onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>
                                                                    <div>신고</div>
                                                                    <div onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)}>{comment.like}</div>
                                                                </div>
                                                            )
                                                        })
                                                    )
                                            }
                                        </div>
                                    </div>) : (
                                        <>
                                            <Text data={feed.body}></Text>
                                            <ol className={style['quiz_box']}>
                                                {
                                                    feed.choice.map((choi, i) => {
                                                        return (
                                                            <li key={i}>{i + 1}. {choi}
                                                                <span>{feed.result[i]}</span>
                                                            </li>
                                                            // <li key={i}>{i + 1}. {choice}</li>
                                                        )
                                                    })
                                                }
                                            </ol>
                                        </>)
                            }

                        </div>

                        <div style={{ width: '100%', height: '20px' }}></div>

                        {
                            func && (
                                <div className={style['function_box']}>
                                    {
                                        isClickedMoreSee ? (<div onClick={handleMoreSee}>본문 보기</div>) : (
                                            <div onClick={(event) => {
                                                handleMoreSee();
                                                handleShowComment(feed.fid, event);
                                            }}>댓글 더보기</div>)
                                    }
                                    <div>신고</div>
                                    <div onClick={(e) => { handleCheckStar(feed.fid, e) }}>좋아요 {feed.star}</div>
                                </div>
                            )
                        }
                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData}></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'balance' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <div>
                            <InfoArea color={'#60E7EC'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        <div className={style['comments_box']}>
                                            {
                                                allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                                    (
                                                        allComments.map((comment, i) => {
                                                            return (
                                                                <div key={comment.cid} className={style['comment']} on>
                                                                    <div>{i}</div>
                                                                    <div>{comment.uname}</div>
                                                                    <div>{comment.body}</div>
                                                                    <div onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>
                                                                    <div>신고</div>
                                                                    <div onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)}>{comment.like}</div>
                                                                </div>
                                                            )
                                                        })
                                                    )
                                            }
                                        </div>

                                    </div>) : (
                                        <>
                                            <Text data={feed.body}></Text>
                                            <div className={style['button_container']}>
                                                <button className={style['select_button']} onClick={(event) => handleInteraction(event, feed.fid)}>{feed.choice[0]} 결과{feed.result[0]}</button>
                                                <button className={style['select_button']}>{feed.choice[1]} 결과{feed.result[1]}</button>
                                            </div>
                                        </>)
                            }

                        </div>
                        <div style={{ width: '100%', height: '20px' }}></div>

                        {
                            func && (
                                <div className={style['function_box']}>
                                    {
                                        isClickedMoreSee ? (<div onClick={handleMoreSee}>본문 보기</div>) : (
                                            <div onClick={(event) => {
                                                handleMoreSee();
                                                handleShowComment(feed.fid, event);
                                            }}>댓글 더보기</div>)
                                    }
                                    <div>신고</div>
                                    <div onClick={(e) => { handleCheckStar(feed.fid, e) }}>좋아요 {feed.star}</div>
                                </div>
                            )
                        }
                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData}></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'station' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <div>
                            <InfoArea color={'#78D2C8'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        <div className={style['comments_box']}>
                                            {
                                                allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                                    (
                                                        allComments.map((comment, i) => {
                                                            return (
                                                                <div key={comment.cid} className={style['comment']} on>
                                                                    <div>{i}</div>
                                                                    <div>{comment.uname}</div>
                                                                    <div>{comment.body}</div>
                                                                    <div onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>
                                                                    <div>신고</div>
                                                                    <div onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)}>{comment.like}</div>
                                                                </div>
                                                            )
                                                        })
                                                    )
                                            }
                                        </div>
                                    </div>) : (
                                        <>
                                            <Text data={feed.body}></Text>
                                            <div className={style['link_box']}>
                                                <h1>{feed.choice[0]}</h1>
                                                <h5>{feed.choice[1]}</h5>
                                            </div>
                                        </>
                                    )
                            }

                        </div>
                        <div style={{ width: '100%', height: '20px' }}></div>
                        {
                            func && (
                                <div className={style['function_box']}>
                                    {
                                        isClickedMoreSee ? (<div onClick={handleMoreSee}>본문 보기</div>) : (
                                            <div onClick={(event) => {
                                                handleMoreSee();
                                                handleShowComment(feed.fid, event);
                                            }}>댓글 더보기</div>)
                                    }
                                    <div>신고</div>
                                    <div onClick={(e) => { handleCheckStar(feed.fid, e) }}>좋아요 {feed.star}</div>
                                </div>
                            )
                        }
                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData}></Comments>
                    </div>
                )
            }
        </>


        //        
        //     {
        //         feed.fclass === 'i' && (
        //             <div className={style.feed}>
        //                 <div className={style['info_area']}>
        //                     <div className={style['planet_name']}>
        //                         <p className={style['sup_people']}>익명지지자</p>
        //                         <img src={planet1}></img>
        //                         <p>정거장 행성</p>
        //                     </div>
        //                 </div>
        //                 {/* <Text></Text> */}
        //             </div>
        //         )
        //     }
        //     {
        //         feed.fclass === 'ad' && (
        //             <div className={style.feed}>
        //                 <div className={style['info_area']}>
        //                     <div className={style['planet_name']}>
        //                         <img src={planet1}></img>
        //                         <p>정거장 행성</p>
        //                     </div>
        //                     <p className={style['sup_people']}>익명지지자</p>
        //                 </div>
        //                 {/* <Text></Text> */}
        //             </div>
        //         )
        //     }
        // </>
    )
}

export function InfoArea({ color, name, date, supporter }) {

    return (
        <div className={style['info_area']}>
            <div className={style['top_part']}>
                <div className={style['planet_name']}>
                    {/* <img src={img}></img> */}
                    <div className={style.circle} style={{ background: `${color}` }}></div>
                    <p>{name}</p>
                    <p className={style['write-date']}>{date}</p>
                </div>
                <p className={style['sup_people']}>{supporter}</p>
            </div>

        </div>
    )
}

export function Text({ name, data }) {

    return (
        <div style={{ height: '100px', marginLeft: '20px' }}>
            {
                !name && <p>{data}</p>
            }

        </div>
    )
}

export function Comments({ isClickedComment, feed, allComments, setAllComments, setFeedData }) {
    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }

    let [inputValue, setInputValue] = useState('');

    function handleChange(e) {
        setInputValue(e.target.value);
    };

    function handleSubmit(fid, event) {
        event.preventDefault();

        fetch('https://nova-platform.kr/feed_explore/make_comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                header,
            },
            credentials: 'include',
            body: JSON.stringify({
                header: header,
                body: {
                    fid: `${feed.fid}`,
                    body: `${inputValue}`
                }
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // setNewComments(data.body.comments);
                setAllComments((prevAllComments) => {
                    const newAllComments = [data.body.comments[0], ...prevAllComments];
                    return newAllComments;
                })
                setFeedData((prevFeeds) => {
                    return prevFeeds.map((feed) => {
                        return feed.fid === fid ? { ...feed, num_comment: data.body.feed[0].num_comment } : feed
                    })
                })
                setInputValue('');
                console.log('asdjljsdlasdajld', allComments);
            })
    }



    return (
        <div className={style['comment_container']}>
            <div className={style['comment_box']}>
                {
                    allComments.length === 0 ? (
                        <>
                            <div className={style['comment_support']}>{feed.comment.uname}</div>
                            <div className={style['comment_data']}>{feed.comment.body}</div>

                        </>
                    ) :
                        !isClickedComment && (
                            <>
                                <div className={style['comment_support']}>{allComments[0].uname}</div>
                                <div className={style['comment_data']}>{allComments[0].body}</div>
                            </>
                        )
                }
            </div>
            <div className={style['comment_action']}>
                <form onSubmit={(event) => handleSubmit(feed.fid, event)}>
                    <input type='text' value={inputValue} onChange={handleChange}></input>
                    <button type='submit'>댓글 작성</button>
                </form>
            </div>

        </div>
    )
}

export function InputFeed() {
    return (
        <div className={`${style['input_feed']}`}>
            <div className={style['input_title']}>
                <input type='text' placeholder='글 제목'></input>
            </div>
            <div className={style['input_content']}>
                <div className={style['content_container']}>
                    {/* 글 내용 박스는 정거장과 퀴즈일때 안보여야 됨 */}
                    <textarea type='text' placeholder='글 내용'></textarea>
                    {/* 정거장 */}
                    {/* <div className={style.station}>
                        <input type='text' placeholder='사이트 이름'></input>
                        <input type='text' placeholder='링크 설명'></input>
                        <input type='url' placeholder='링크 주소'></input>
                    </div> */}
                    {/* 퀴즈  */}
                    {/* <div className={style['input_quiz_box']}>
                        <input type='text' placeholder='목록1'></input>
                        <input type='text' placeholder='목록2'></input>
                        <input type='text' placeholder='목록3'></input>
                        <input type='text' placeholder='목록4'></input>
                    </div> */}
                    {/* 이지선다 */}
                    <div className={style['input_button_container']}>
                        <input className={style['select_button']} placeholder='선택지1'></input>
                        <input className={style['select_button']} placeholder='선택지2'></input>
                    </div>
                    {/* 일반 */}
                    {/* <input type='text'></input> */}
                    <div className={style['submit_area']}>
                        <button type='submit' className={style['submit_button']}>작성 완료</button>
                        <h6>타인에게 불편을 줄 수 있는 내용의 게시글은 경고없이 삭제될 수 있습니다.</h6>
                    </div>
                </div>

            </div>
        </div>
    )
}