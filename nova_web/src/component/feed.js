import style from './../pages/FeedPage/FeedPage.module.css';
// import planet1 from './../img/planet1.png';
// import planet2 from './../img/planet2.png';
// import planet3 from './../img/planet3.png';
// import planet4 from './../img/planet4.png';
import { useState } from 'react';
// import {}
import { FaStar } from "react-icons/fa";

// import { useRef, useState } from 'react';

export default function Feed({ className, feed, func, feedData, setFeedData, img_circle, isUserState }) {

    // function handleRequestURL() {
    //     window.open(requestURL, '_blank', "noopener, noreferrer");
    // };

    // let [isInteraction, setIsInteraction] = useState(false);
    let [selectedIndex, setSelectedIndex] = useState(null);
    let [isError, setIsError] = useState();
    // let [myAttend, setMyAttend] = useState(null);

    const handleClick = (index) => {

        if (selectedIndex === index) {
            setSelectedIndex(null);
        } else {
            setSelectedIndex(index);
        }
    };

    function handleInteraction(event, fid, action) {
        event.preventDefault();

        fetch(`https://nova-platform.kr/feed_explore/interaction_feed?fid=${fid}&action=${action}`, {
            credentials: 'include'
        })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        setIsError(response.status);
                    } else {
                        throw new Error(`status: ${response.status}`)
                    }
                }
                return response.json()
            })
            .then(data => {
                console.log(data);
                // setMyAttend(data.body.feed[0].attend);
                setFeedData((prevFeeds) => {
                    return prevFeeds.map((feed) => {
                        return feed.fid === fid ? { ...feed, attend: data.body.feed[0].attend, result: data.body.feed[0].result } : feed
                    })
                })
            })
    }

    // 댓글 더보기 - 본문 보기
    let [isClickedMoreSee, setIsClickedMoreSee] = useState(false);

    function handleMoreSee() {
        setIsClickedMoreSee(!isClickedMoreSee);
    };


    let [isClickedStar, setIsClickedStar] = useState(false);

    function handleCheckStar(fid, e) {
        // e.preventDefault();
        setIsClickedStar(!isClickedStar);
        fetch(`https://nova-platform.kr/feed_explore/check_star?fid=${fid}`, {
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        setIsError(response.status);
                    } else {
                        throw new Error(`status: ${response.status}`)
                    }
                }
                return response.json()
            })
            .then(data => {
                console.log('clickstar', data)
                setFeedData((prevFeeds) => {
                    return prevFeeds.map((feed) => {
                        return feed.fid === fid ? { ...feed, star_flag: data.body.feed[0].star_flag, star: data.body.feed[0].star } : feed
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
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        setIsError(response.status);
                    } else {
                        throw new Error(`status: ${response.status}`)
                    }
                }
                return response.json()
            })
            .then(data => {
                console.log('like', data.body.comments);

                setAllComments((prevAll) => {
                    return prevAll.map((comment, i) => {
                        return comment.cid === cid ? { ...comment, like: data.body.comments[i].like, like_user: data.body.comments[i].like_user } : comment
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
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        setIsError(response.status);
                    } else {
                        throw new Error(`status: ${response.status}`)
                    }
                }
                return response.json()
            })
            .then(data => {
                console.log('remove', data.body.comments);
                // setAllComments((prevAll)=>{
                //     const newAllComments = [data.body.comments];
                //     return newAllComments;
                // })
            })
    }

    return (
        <>
            {
                feed.fclass === 'card' &&
                (
                    <div className={`${style.feed} ${className}`} >
                        <div>
                            {
                                img_circle && <div style={{ height: '80px' }}></div>
                            }
                            <InfoArea color={'#7960EC'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>

                                        {allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                            (
                                                allComments.map((comment, i) => {
                                                    return (
                                                        <div className={style['comments_box']}>
                                                            <div key={comment.cid} className={style['comment']}>
                                                                <div className={style['user_name']}>
                                                                    <div>{comment.uname}</div>
                                                                    <div className={style['interaction_btn']}>
                                                                        {
                                                                            comment.owner ? (<div className={style['delete_btn']} onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>) : (<div className={style['delete_btn']}></div>)
                                                                        }
                                                                        <div className={style['report_star_btn']}>
                                                                            <div className={style.report}>신고</div>
                                                                            <div className={style['star_num']}>
                                                                                {
                                                                                    isUserState ? (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)} />
                                                                                    ) : (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(e) => {
                                                                                                e.preventDefault()
                                                                                                alert('로그인을 해주세요.')
                                                                                            }} />
                                                                                    )
                                                                                }
                                                                                <div style={{ marginLeft: '2px' }}>
                                                                                    {comment.like}
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className={style['comment_text']}>{comment.body}</div>
                                                            </div>
                                                        </div>
                                                    )
                                                })
                                            )}

                                    </div>) : <>
                                        <Text data={feed.body}></Text>
                                        {
                                            !img_circle &&
                                            <div className={style['home_feed_img']}>
                                                {/* 1개이미지 */}
                                                {
                                                    feed.num_image === 1 && (
                                                        <img src={feed.image[0]} alt='img' />
                                                    )
                                                }
                                                {/* 2개이미지 */}
                                                {
                                                    feed.num_image === 2 && (
                                                        <div className={style['image-box']}>
                                                            <div className={`${style["image-show"]} ${style['two-image']}`}>
                                                                {feed.image.map((img, i) => {
                                                                    return (
                                                                        <img key={i} src={img} alt='img' />
                                                                    )
                                                                })}
                                                            </div>
                                                        </div>
                                                    )
                                                }
                                                {/* 3개이미지 */}
                                                {
                                                    feed.num_image === 3 && (
                                                        <div className={style['image-box']}>
                                                            <div className={`${style["image-show"]} ${style['three-image']}`}>
                                                                {feed.image.map((img, i) => {
                                                                    return (
                                                                        <img key={i} src={img} alt='img' />
                                                                    )
                                                                })}
                                                            </div>
                                                        </div>
                                                    )
                                                }
                                                {/* 4개이미지 */}
                                                {
                                                    feed.num_image === 4 && (
                                                        <div className={style['image-show']}>
                                                            {feed.image.map((img, i) => {
                                                                return (
                                                                    <img key={i} src={img} alt='img' />
                                                                )
                                                            })}
                                                        </div>
                                                    )
                                                }
                                                {/* 5개이상 */}
                                                {
                                                    feed.num_image >= 5 && (
                                                        <div className={style['image-box']}>
                                                            <div className={`${style["image-origin"]} ${style['five-over-image']}`}>
                                                                {feed.image.map((img, i) => {
                                                                    return (
                                                                        <img key={i} src={img} alt="이미지" />
                                                                    )
                                                                })}
                                                            </div>
                                                        </div>
                                                    )
                                                }
                                            </div>

                                        }
                                    </>
                            }
                        </div>
                        <div style={{ width: '100%', height: '50px' }}></div>
                        {
                            func && (
                                <div className={style['function_box']}>
                                    <div className={style['action_btn']}>
                                        {
                                            isClickedMoreSee ? (<div className={style['show_body']} onClick={handleMoreSee}>본문 보기</div>) : (
                                                <>
                                                    <div className={style['show_body']}
                                                        onClick={(event) => {
                                                            handleMoreSee();
                                                            handleShowComment(feed.fid, event);
                                                        }}>댓글 더보기</div>
                                                    <div className={style['report_btn']}>신고</div>
                                                </>
                                            )
                                        }
                                    </div>
                                    <div className={style['like_btn']}>
                                        {
                                            isUserState ? (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => { handleCheckStar(feed.fid, e) }} />
                                            ) : (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => {
                                                        e.preventDefault()
                                                        alert('로그인이 필요합니다.')
                                                    }} />
                                            )
                                        }
                                        <div className={style['num_like']}>{feed.star}</div>
                                    </div>
                                </div>
                            )
                        }

                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData} isUserState={isUserState}></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'multiple' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <div>
                            {
                                img_circle && <div style={{ height: '80px' }}></div>
                            }
                            <InfoArea color={'#E370D1'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        {allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                            (
                                                allComments.map((comment, i) => {
                                                    return (
                                                        <div className={style['comments_box']}>
                                                            <div key={comment.cid} className={style['comment']}>
                                                                <div className={style['user_name']}>
                                                                    <div>{comment.uname}</div>
                                                                    <div className={style['interaction_btn']}>
                                                                        {
                                                                            comment.owner ? (<div className={style['delete_btn']} onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>) : (<div className={style['delete_btn']}></div>)
                                                                        }
                                                                        <div className={style['report_star_btn']}>
                                                                            <div className={style.report}>신고</div>
                                                                            <div className={style['star_num']}>
                                                                                {
                                                                                    isUserState ? (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)} />
                                                                                    ) : (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(e) => {
                                                                                                e.preventDefault()
                                                                                                alert('로그인을 해주세요.')
                                                                                            }} />
                                                                                    )
                                                                                }
                                                                                <div style={{ marginLeft: '2px' }}>
                                                                                    {comment.like}
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className={style['comment_text']}>{comment.body}</div>
                                                            </div>
                                                        </div>
                                                    )
                                                })
                                            )}
                                    </div>) : (
                                        <>
                                            <Text data={feed.body}></Text>
                                            {
                                                !img_circle &&
                                                <div className={style['home_feed_img']}>
                                                    {/* 1개이미지 */}
                                                    {
                                                        feed.num_image === 1 && (
                                                            <img src={feed.image[0]} alt='img' />
                                                        )
                                                    }
                                                    {/* 2개이미지 */}
                                                    {
                                                        feed.num_image === 2 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-show"]} ${style['two-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt='img' />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                    {/* 3개이미지 */}
                                                    {
                                                        feed.num_image === 3 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-show"]} ${style['three-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt='img' />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                    {/* 4개이미지 */}
                                                    {
                                                        feed.num_image === 4 && (
                                                            <div className={style['image-show']}>
                                                                {feed.image.map((img, i) => {
                                                                    return (
                                                                        <img key={i} src={img} alt='img' />
                                                                    )
                                                                })}
                                                            </div>
                                                        )
                                                    }
                                                    {/* 5개이상 */}
                                                    {
                                                        feed.num_image >= 5 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-origin"]} ${style['five-over-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt="이미지" />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }

                                                </div>
                                            }
                                            <ol className={style['quiz_box']}>
                                                {
                                                    feed.choice.map((choi, i) => {

                                                        if (feed.attend === i) {
                                                            if (isUserState) {
                                                                return (
                                                                    <li onClick={(e) => {
                                                                        handleInteraction(e, feed.fid, i)
                                                                        handleClick(i);
                                                                    }} key={i} style={{ backgroundColor: i === feed.attend ? '#D2C8F7' : 'white' }}>{i + 1}. {choi}
                                                                        <span>{feed.result[i]}</span>
                                                                    </li>
                                                                )
                                                            } else {
                                                                return (
                                                                    <li onClick={(e) => {
                                                                        e.preventDefault();
                                                                        alert('로그인이 필요합니다.')
                                                                    }} key={i} style={{ backgroundColor: i === feed.attend ? '#D2C8F7' : 'white' }}>{i + 1}. {choi}
                                                                        <span>{feed.result[i]}</span>
                                                                    </li>
                                                                )
                                                            }

                                                        } else {
                                                            if (isUserState) {
                                                                return (
                                                                    <li onClick={(e) => {
                                                                        handleInteraction(e, feed.fid, i)
                                                                        handleClick(i);
                                                                    }} key={i} style={{ backgroundColor: selectedIndex === i ? '#D2C8F7' : 'white' }}>{i + 1}. {choi}
                                                                        {
                                                                            feed.attend !== -1 ? <span>{feed.result[i]}</span> : <span></span>
                                                                        }
                                                                    </li>
                                                                )
                                                            } else {
                                                                return (
                                                                    <li onClick={(e) => {
                                                                        e.preventDefault();
                                                                        alert('로그인이 필요합니다.')
                                                                    }} key={i} style={{ backgroundColor: selectedIndex === i ? '#D2C8F7' : 'white' }}>{i + 1}. {choi}
                                                                        {
                                                                            feed.attend !== -1 ? <span>{feed.result[i]}</span> : <span></span>
                                                                        }
                                                                    </li>
                                                                )
                                                            }

                                                        }
                                                        // <li key={i}>{i + 1}. {choice}</li>
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
                                    <div className={style['action_btn']}>
                                        {
                                            isClickedMoreSee ? (<div className={style['show_body']} onClick={handleMoreSee}>본문 보기</div>) : (
                                                <>
                                                    <div className={style['show_body']}
                                                        onClick={(event) => {
                                                            handleMoreSee();
                                                            handleShowComment(feed.fid, event);
                                                        }}>댓글 더보기</div>
                                                    <div className={style['report_btn']}>신고</div>
                                                </>
                                            )
                                        }
                                    </div>
                                    <div className={style['like_btn']}>
                                        {
                                            isUserState ? (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => { handleCheckStar(feed.fid, e) }} />
                                            ) : (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => {
                                                        e.preventDefault()
                                                        alert('로그인이 필요합니다.')
                                                    }} />
                                            )
                                        }
                                        <div className={style['num_like']}>{feed.star}</div>
                                    </div>
                                </div>
                            )
                        }
                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData} isUserState={isUserState}></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'balance' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <div>
                            {
                                img_circle && <div style={{ height: '80px' }}></div>
                            }
                            <InfoArea color={'#60E7EC'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        {allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                            (
                                                allComments.map((comment, i) => {
                                                    return (
                                                        <div className={style['comments_box']}>
                                                            <div key={comment.cid} className={style['comment']}>
                                                                <div className={style['user_name']}>
                                                                    <div>{comment.uname}</div>
                                                                    <div className={style['interaction_btn']}>
                                                                        {
                                                                            comment.owner ? (<div className={style['delete_btn']} onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>) : (<div className={style['delete_btn']}></div>)
                                                                        }
                                                                        <div className={style['report_star_btn']}>
                                                                            <div className={style.report}>신고</div>
                                                                            <div className={style['star_num']}>
                                                                                {
                                                                                    isUserState ? (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)} />
                                                                                    ) : (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(e) => {
                                                                                                e.preventDefault()
                                                                                                alert('로그인을 해주세요.')
                                                                                            }} />
                                                                                    )
                                                                                }
                                                                                <div style={{ marginLeft: '2px' }}>
                                                                                    {comment.like}
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className={style['comment_text']}>{comment.body}</div>
                                                            </div>
                                                        </div>
                                                    )
                                                })
                                            )}

                                    </div>) : (
                                        <>
                                            <Text data={feed.body}></Text>
                                            {
                                                !img_circle &&
                                                <div className={style['home_feed_img']}>
                                                    {/* 1개이미지 */}
                                                    {
                                                        feed.num_image === 1 && (
                                                            <img src={feed.image[0]} alt='img' />
                                                        )
                                                    }
                                                    {/* 2개이미지 */}
                                                    {
                                                        feed.num_image === 2 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-show"]} ${style['two-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt='img' />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                    {/* 3개이미지 */}
                                                    {
                                                        feed.num_image === 3 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-show"]} ${style['three-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt='img' />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                    {/* 4개이미지 */}
                                                    {
                                                        feed.num_image === 4 && (
                                                            <div className={style['image-show']}>
                                                                {feed.image.map((img, i) => {
                                                                    return (
                                                                        <img key={i} src={img} alt='img' />
                                                                    )
                                                                })}
                                                            </div>
                                                        )
                                                    }
                                                    {/* 5개이상 */}
                                                    {
                                                        feed.num_image >= 5 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-origin"]} ${style['five-over-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt="이미지" />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }

                                                </div>
                                            }
                                            <div className={style['button_container']}>
                                                {
                                                    feed.choice.map((sel, i) => {
                                                        return (
                                                            <div key={feed.fid + i}>
                                                                <div>
                                                                    {
                                                                        isUserState ? (
                                                                            <button className={style['select_button']} onClick={(event) => {
                                                                                handleInteraction(event, feed.fid, i)
                                                                                handleClick(i)
                                                                            }
                                                                            } style={{ backgroundColor: i === feed.attend ? '#D2C8F7' : 'white' }}>
                                                                                {sel} <br />
                                                                                {
                                                                                    feed.attend !== -1 ? <span>{feed.result[i]}명</span> : <span></span>
                                                                                }
                                                                            </button>
                                                                        ) : (
                                                                            <button className={style['select_button']} onClick={(e) => {
                                                                                e.preventDefault();
                                                                                alert('로그인이 필요합니다.')
                                                                            }
                                                                            } style={{ backgroundColor: i === feed.attend ? '#D2C8F7' : 'white' }}>
                                                                                {sel} <br />
                                                                                {
                                                                                    feed.attend !== -1 ? <span>{feed.result[i]}명</span> : <span></span>
                                                                                }
                                                                            </button>
                                                                        )
                                                                    }

                                                                </div>

                                                            </div>
                                                            // <button className={style['select_button']}>{feed.choice[1]} 결과{feed.result[1]}</button>

                                                        )
                                                    })
                                                }
                                            </div>
                                        </>)
                            }

                        </div>
                        <div style={{ width: '100%', height: '20px' }}></div>

                        {
                            func && (
                                <div className={style['function_box']}>
                                    <div className={style['action_btn']}>
                                        {
                                            isClickedMoreSee ? (<div className={style['show_body']} onClick={handleMoreSee}>본문 보기</div>) : (
                                                <>
                                                    <div className={style['show_body']}
                                                        onClick={(event) => {
                                                            handleMoreSee();
                                                            handleShowComment(feed.fid, event);
                                                        }}>댓글 더보기</div>
                                                    <div className={style['report_btn']}>신고</div>
                                                </>
                                            )
                                        }
                                    </div>
                                    <div className={style['like_btn']}>
                                        {
                                            isUserState ? (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => { handleCheckStar(feed.fid, e) }} />
                                            ) : (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => {
                                                        e.preventDefault()
                                                        alert('로그인이 필요합니다.')
                                                    }} />
                                            )
                                        }
                                        <div className={style['num_like']}>{feed.star}</div>
                                    </div>
                                </div>
                            )
                        }
                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData} isUserState={isUserState}></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'station' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <div>
                            {
                                img_circle && <div style={{ height: '80px' }}></div>
                            }

                            <InfoArea color={'#78D2C8'} name={`${feed.class_name} 행성`} date={feed.date} supporter={`${feed.nickname}`}></InfoArea>
                            {
                                isClickedMoreSee ?
                                    (<div className={style['more_comments']}>
                                        {allComments.length === 0 ? <div>댓글이 없습니다.</div> :
                                            (
                                                allComments.map((comment, i) => {
                                                    return (
                                                        <div className={style['comments_box']}>
                                                            <div key={comment.cid} className={style['comment']}>
                                                                <div className={style['user_name']}>
                                                                    <div>{comment.uname}</div>
                                                                    <div className={style['interaction_btn']}>
                                                                        {
                                                                            comment.owner ? (<div className={style['delete_btn']} onClick={(event) => handleRemoveComment(comment.fid, comment.cid, event)}>삭제</div>) : (<div className={style['delete_btn']}></div>)
                                                                        }
                                                                        <div className={style['report_star_btn']}>
                                                                            <div className={style.report}>신고</div>
                                                                            <div className={style['star_num']}>
                                                                                {
                                                                                    isUserState ? (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)} />
                                                                                    ) : (
                                                                                        <FaStar className={style['comment_like']} style={comment.like_user ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                                                            onClick={(e) => {
                                                                                                e.preventDefault()
                                                                                                alert('로그인을 해주세요.')
                                                                                            }} />
                                                                                    )
                                                                                }
                                                                                <div style={{ marginLeft: '2px' }}>
                                                                                    {comment.like}
                                                                                </div>
                                                                            </div>
                                                                            {/* <div onClick={(event) => handleCommentLike(comment.fid, comment.cid, event)}>{comment.like}</div> */}
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div className={style['comment_text']}>{comment.body}</div>
                                                            </div>
                                                        </div>
                                                    )
                                                })
                                            )}
                                    </div>) : (
                                        <>
                                            <Text data={feed.body}></Text>
                                            {
                                                !img_circle &&
                                                <div className={style['home_feed_img']}>
                                                    {/* 1개이미지 */}
                                                    {
                                                        feed.num_image === 1 && (
                                                            <img src={feed.image[0]} alt='img' />
                                                        )
                                                    }
                                                    {/* 2개이미지 */}
                                                    {
                                                        feed.num_image === 2 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-show"]} ${style['two-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt='img' />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                    {/* 3개이미지 */}
                                                    {
                                                        feed.num_image === 3 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-show"]} ${style['three-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt='img' />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                    {/* 4개이미지 */}
                                                    {
                                                        feed.num_image === 4 && (
                                                            <div className={style['image-show']}>
                                                                {feed.image.map((img, i) => {
                                                                    return (
                                                                        <img key={i} src={img} alt='img' />
                                                                    )
                                                                })}
                                                            </div>
                                                        )
                                                    }
                                                    {/* 5개이상 */}
                                                    {
                                                        feed.num_image >= 5 && (
                                                            <div className={style['image-box']}>
                                                                <div className={`${style["image-origin"]} ${style['five-over-image']}`}>
                                                                    {feed.image.map((img, i) => {
                                                                        return (
                                                                            <img key={i} src={img} alt="이미지" />
                                                                        )
                                                                    })}
                                                                </div>
                                                            </div>
                                                        )
                                                    }
                                                </div>
                                            }

                                            <div className={style['link_box']}
                                                onClick={() => {
                                                    window.open(feed.choice[2], '_blank', "noopener, noreferrer");
                                                }}>
                                                <h1>{feed.choice[0]}</h1>
                                                <h5>{feed.choice[1]}</h5>
                                                {/* <h5>{feed.choice[2]}</h5> */}
                                            </div>
                                        </>
                                    )
                            }

                        </div>
                        <div style={{ width: '100%', height: '20px' }}></div>
                        {
                            func && (
                                <div className={style['function_box']}>
                                    <div className={style['action_btn']}>
                                        {
                                            isClickedMoreSee ? (<div className={style['show_body']} onClick={handleMoreSee}>본문 보기</div>) : (
                                                <>
                                                    <div className={style['show_body']}
                                                        onClick={(event) => {
                                                            handleMoreSee();
                                                            handleShowComment(feed.fid, event);
                                                        }}>댓글 더보기</div>
                                                    <div className={style['report_btn']}>신고</div>
                                                </>
                                            )
                                        }
                                    </div>
                                    <div className={style['like_btn']}>
                                        {
                                            isUserState ? (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => { handleCheckStar(feed.fid, e) }} />
                                            ) : (
                                                <FaStar className={style.like} style={feed.star_flag ? { fill: 'yellow' } : { fill: 'white', stroke: 'black', strokeWidth: '25' }}
                                                    onClick={(e) => {
                                                        e.preventDefault()
                                                        alert('로그인이 필요합니다.')
                                                    }} />
                                            )
                                        }
                                        <div className={style['num_like']}>{feed.star}</div>
                                    </div>
                                </div>
                            )
                        }
                        <div className={style.line}></div>
                        <Comments feed={feed} allComments={allComments} setAllComments={setAllComments} setFeedData={setFeedData} isUserState={isUserState}></Comments>
                    </div>
                )
            }



        </>
    )
}

export function InfoArea({ color, name, date, supporter }) {

    return (
        <div className={style['info_area']}>
            <div className={style['top_part']}>
                <div className={style['planet_name']}>
                    {/* <img src={img}></img> */}
                    {/* <div className={style.circle} style={{ background: `${color}` }}></div> */}
                    {/*<p>{name}</p>*/}
                    <p className={style['write-date']}>{date}</p>
                </div>
                <p className={style['sup_people']}>{supporter}</p>
            </div>

        </div>
    )
}

export function Text({ name, data }) {

    return (
        <div style={{ height: '100px', marginLeft: '20px', color: '#FFFFFF' }}>
            {
                !name && <p>{data}</p>
            }

        </div>
    )
}

export function Comments({ isClickedComment, feed, allComments, setAllComments, setFeedData, isUserState }) {
    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }
    let [isError, setIsError] = useState();

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
                // console.log('asdjljsdlasdajld', allComments);
            })
    }



    return (
        <div className={style['comment_container']}>
            <div className={style['comment_box']}>
                {
                    allComments.length === 0 ? (
                        <>
                            {/* <div className={style['comment_support']}>{feed.comment.uname}</div> */}
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