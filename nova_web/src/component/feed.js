import style from './../pages/FeedPage/FeedPage.module.css';
import planet1 from './../img/planet1.png';
import planet2 from './../img/planet2.png';
import planet3 from './../img/planet3.png';
import planet4 from './../img/planet4.png';
// import { useRef, useState } from 'react';

export default function Feed({ type, className}) {
    
    // type별 행성
    // -A: 정거장행성
    // -B: 자랑 행성
    // -C: 이지선다 행성
    // -D: 퀴즈 행성
    // -ad or i: 광고 이미지

    return (
        <>
            {
                 (
                    <div className={`${style.feed} ${className}`}>
                        <InfoArea img={planet1} name={'정거장 행성'}></InfoArea>
                        <Text name={'정거장 행성'}></Text>
                        <div className={style['link_box']}>
                            <h1>외부 사이트 링크</h1>
                            <h5>큐떱 짧툰 8화</h5>
                        </div>
                    </div>
                )
            }
            {
                type === '2' && (
                    <div className={style.feed}>
                        <InfoArea img={planet2} name={'자랑 행성'}></InfoArea>
                        <Text></Text>
                    </div>
                )
            }
            {
                type === '3' && (
                    <div className={style.feed}>
                        <InfoArea img={planet3} name={'이지선다 행성'}></InfoArea>
                        <Text></Text>
                        <div className={style['button_container']}>
                            <button className={style['select_button']}>갑니다</button>
                            <button className={style['select_button']}>패스</button>
                        </div>
                    </div>
                )
            }
            {
                type === '4' && (
                    <div className={style.feed}>
                        <InfoArea img={planet4} name={'퀴즈 행성'}></InfoArea>
                        <Text name={'퀴즈 행성'}></Text>
                        <ol className={style['quiz_box']}>
                            <li>1. 드라마</li>
                            <li>2. Super Nova</li>
                            <li>3. 만찬가</li>
                            <li>4. 여섯번째 여름</li>
                        </ol>
                    </div>
                )
            }
            {
                type === 'i' && (
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
            {
                type === 'ad' && (
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

function InfoArea({ img, name }) {

    return (
        <div className={style['info_area']}>
            <div className={style['planet_name']}>
                <img src={img}></img>
                <p>{name}</p>
            </div>
            <p className={style['sup_people']}>익명지지자</p>
        </div>
    )
}

function Text({ name }) {

    return (
        <div style={{ marginLeft: '20px' }}>
            <h1 className={style.title}>글 제목</h1>
            {
                !name && <p>글 내용</p>
            }

        </div>
    )
}

export function InputFeed() {
    return (
        <div className={`${style['input_feed']}` }>
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