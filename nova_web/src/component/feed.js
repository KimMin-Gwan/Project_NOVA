import style from './../pages/FeedPage/FeedPage.module.css';
import planet1 from './../img/planet1.png';
import planet2 from './../img/planet2.png';
import planet3 from './../img/planet3.png';
import planet4 from './../img/planet4.png';
// import { useRef, useState } from 'react';

export default function Feed({ className, feed }) {

    return (
        <>
            {
                //클릭시 링크 이동 수정 필요
                feed.fclass === 'station' &&
                (
                    <div className={`${style.feed} ${className}`}>
                        <InfoArea color={'#78D2C8'} name={`${feed.class_name} 행성`} supporter={feed.nickname}></InfoArea>
                        <Text name={`${feed.class_name} 행성`} title={feed.title}></Text>
                        <div className={style['link_box']}>
                            <h1>{feed.choice[0]}</h1>
                            <h5>{feed.choice[1]}</h5>
                        </div>
                        
                        <div style={{ width: '100%', height: '20px' }}></div>
                        <div className={style.line}>
                            <div className={style['comment_function']}>
                                <div>댓글 더보기</div>
                                <div>신고</div>
                            </div>
                            <div>1.6k</div>
                        </div>
                        <Comments></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'card' && (
                    <div className={style.feed}>
                        <InfoArea color={'#7960EC'} name={`${feed.class_name} 행성`} supporter={feed.nickname}></InfoArea>
                        <Text title={feed.title} data={feed.body}></Text>

                        <div style={{ width: '100%', height: '50px' }}></div>
                        <div className={style.line}>
                            <div className={style['comment_function']}>
                                <div>댓글 더보기</div>
                                <div>신고</div>
                            </div>
                            <div>1.6k</div>
                        </div>
                        <Comments></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'balance' && (
                    <div className={style.feed}>
                        <InfoArea color={'#60E7EC'} name={`${feed.class_name} 행성`} supporter={feed.nickname}></InfoArea>
                        <Text title={feed.title}></Text>
                        <div className={style['button_container']}>
                            <button className={style['select_button']}>갑니다</button>
                            <button className={style['select_button']}>패스</button>
                        </div>

                        {/* <div style={{ width: '100%', height: '20px' }}></div> */}
                        {/* <div className={style.line}>
                            <div className={style['comment_function']}>
                                <div>댓글 더보기</div>
                                <div>신고</div>
                            </div>
                            <div>1.6k</div>
                        </div>
                        <Comments></Comments> */}
                    </div>
                )
            }
            {
                feed.fclass === 'multiple' && (
                    <div className={style.feed}>
                        <InfoArea color={'#E370D1'} name={`${feed.class_name} 행성`} supporter={feed.nickname}></InfoArea>
                        <Text name={'퀴즈 행성'} title={feed.title}></Text>
                        <ol className={style['quiz_box']}>
                            {
                                feed.choice.map((choice, i) => {
                                    if (feed.attend === 0) {
                                        return (
                                            <li key={i}>{i + 1}. {choice}
                                                <span>{feed.result[i]}</span>
                                            </li>
                                        )
                                    } else {
                                        <li key={i}>{i + 1}. {choice}</li>
                                    }
                                })
                            }
                        </ol>
                        <div style={{ width: '100%', height: '50px' }}></div>
                        <div className={style.line}>
                            <div className={style['comment_function']}>
                                <div>댓글 더보기</div>
                                <div>신고</div>
                            </div>
                            <div>1.6k</div>
                        </div>
                        <Comments></Comments>
                    </div>
                )
            }
            {
                feed.fclass === 'i' && (
                    <div className={style.feed}>
                        <div className={style['info_area']}>
                            <div className={style['planet_name']}>
                                <p className={style['sup_people']}>익명지지자</p>
                                <img src={planet1}></img>
                                <p>정거장 행성</p>
                            </div>
                        </div>
                        {/* <Text></Text> */}
                    </div>
                )
            }
            {
                feed.fclass === 'ad' && (
                    <div className={style.feed}>
                        <div className={style['info_area']}>
                            <div className={style['planet_name']}>
                                <img src={planet1}></img>
                                <p>정거장 행성</p>
                            </div>
                            <p className={style['sup_people']}>익명지지자</p>
                        </div>
                        {/* <Text></Text> */}
                    </div>
                )
            }
        </>
    )
}

function InfoArea({color, name, supporter }) {

    return (
        <div className={style['info_area']}>
            <div className={style['top_part']}>
                <div className={style['planet_name']}>
                    {/* <img src={img}></img> */}
                    <div className={style.circle} style={{background:`${color}`}}></div>
                    <p>{name}</p>
                    <p className={style['write-date']}>24/07/23</p>
                </div>
                <p className={style['sup_people']}>{supporter}</p>
            </div>

        </div>
    )
}

function Text({ name, title, data }) {

    return (
        <div style={{ marginLeft: '20px' }}>
            <h1 className={style.title}>{title}</h1>
            {
                !name && <p>{data}</p>
            }

        </div>
    )
}

function Comments({ }) {
    return (
        <div className={style['comment_container']}>
            <div className={style['comment_box']}>
                <div className={style['comment_support']}>바위게게게게게게</div>
                <div className={style['comment_data']}>진짜</div>
            </div>
            <div className={style['comment_action']}>
                <input></input>
                <button>댓글 작성</button>
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