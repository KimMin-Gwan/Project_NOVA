import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import style from './Mypage.module.css';

import { TfiCommentAlt } from "react-icons/tfi";
import { CiStar, CiEdit } from "react-icons/ci";
// import { SlSpeech } from "react-icons/sl";
import { HiOutlineBellAlert } from "react-icons/hi2";
import { IoIosArrowForward, IoIosArrowBack, IoMdCheckmarkCircleOutline } from "react-icons/io";
import { useEffect, useState } from 'react';
// import MySoloBias from '../../component/subscribeBias/mySoloBias';
function MyPage() {

    let bias_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    let navigate = useNavigate();

    let [isClicked, setIsClicked] = useState(false);

    let [mySoloBias, setMySoloBias] = useState([]);
    let [myGroupBias, setMyGroupBias] = useState([]);
    let [myData, setMyData] = useState([]);

    useEffect(() => {
        fetch('https://nova-platform.kr/user_home/my_data', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.body);
                setMySoloBias(data.body.solo_bias);
                setMyGroupBias(data.body.group_bias);
                setMyData(data.body.user);
            })
    }, [])

    function handleClick() {
        setIsClicked(!isClicked);
    };

    useEffect(() => {
        return (
            setIsClicked(false)
        )
    }, []);

    function handleMovePage() {
        navigate('/galaxy')
    };

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>은하계 탐색</div>
            </div>

            <div className={style['base_box']}>
                <div className={style['wrap_box']}>
                    <div className={style['sup_part']}>
                        <div className={style['wrap_sup']}>
                            <div className={style.support}>지지자</div>
                            <div className={style['space_pass']}>우주인 패스 +</div>
                            <div onClick={handleClick}>
                                {
                                    isClicked ? <IoIosArrowBack /> : <IoIosArrowForward />
                                }
                            </div>
                        </div>
                    </div>
                    <div className={style['ticket_part']}>
                        <div className={style['ticket_info']}>
                            <div>별별티켓</div>
                            <div>{myData.credit} 개</div>
                        </div>
                        <div className={style['btn_container']}>
                            <button>충전</button>
                            <button>패스</button>
                        </div>
                    </div>
                </div>
            </div>

            {
                !isClicked &&
                <>
                    <div className={style['base_box']}>
                        <h4>최애-개인</h4>
                        <div className={style['wrap_box']} style={{ flexDirection: 'row', height: 'auto' }}>
                            <div className={style['half_box']}>
                                <div className={`left-box ${style['img_box']}`}>
                                    <div className='image-container'>
                                        <img src={bias_url + `${mySoloBias.bid}.PNG`} alt="bias" className='img2' />
                                    </div>
                                </div>
                            </div>
                            <div className={style['half_box']}>
                                <div className={style['text_box']}>
                                    <p>나의최애</p>
                                    <div className={style['bias_name']}>{mySoloBias.bname}</div>
                                    <div className={style['season_star_dust']}>이번 시즌에 기여한 별가루</div>
                                    <h2>{myData.solo_point} pt</h2>
                                    <button className={style['funding_btn']}>펀딩</button>
                                </div>
                            </div>
                        </div>
                    </div>


                    <div className={style['base_box']}>
                        <div className={style['title_box']}>
                            <h4>최애-단체</h4>
                            <h6>최애 - 단체는 리그와 펀딩을 하지 않아요.</h6>
                        </div>
                        <div className={style['wrap_box']} style={{ flexDirection: 'row', height: 'auto' }}>
                            <div className={style['half_box']}>
                                <div className={`left-box ${style['img_box']}`}>
                                    <div className='image-container'>
                                        <img src={bias_url + `${myGroupBias.bid}.PNG`} alt="bias" className='img2' />
                                    </div>
                                </div>
                            </div>
                            <div className={style['half_box']}>
                                <div className={style['text_box']}>
                                    <p>나의최애</p>
                                    {
                                        myGroupBias.bname === '' ?
                                            (
                                                <div className={style['bias_name']}>아직 최애없음</div>
                                            ) :
                                            (
                                                <div className={style['bias_name']}>{myGroupBias.bname}</div>
                                            )
                                    }
                                    {/* <div className={style['bias_name']}>{myGroupBias.bname === '' && '아직 최애없음'}</div> */}
                                    <div className={style['season_star_dust']}>이번 시즌에 기여한 별가루</div>
                                    <h2>{myData.group_point} pt</h2>
                                    <button className={style['funding_btn']}>펀딩</button>
                                </div>
                            </div>
                        </div>
                    </div>


                    <div className={`${style['base_box']} ${style['height_auto']}`}>
                        <h4>서비스</h4>
                        <div className={style['grid_container']}>
                            <div onClick={handleMovePage}>은하리그</div>
                            <div>노바 펀딩</div>
                            <div>노바 재판</div>
                            <div>노바 알고리즘</div>
                        </div>

                    </div>
                    <div className={`${style['base_box']} ${style['height_auto']}`}>
                        <h4>나의 활동</h4>
                        <div className={style['my_activity']}>
                            <div className={style.activity}>
                                <CiEdit className={style['activity_icon']} />
                                <div>내가 작성한 피드</div>
                                <IoIosArrowForward className={style['activity_icon']} />

                                <CiStar className={style['activity_icon']} />
                                <div>관심 표시한 피드</div>
                                <IoIosArrowForward className={style['activity_icon']} />

                                <TfiCommentAlt className={style['activity_icon']} />
                                <div>댓글을 작성한 피드</div>
                                <IoIosArrowForward className={style['activity_icon']} />

                                <IoMdCheckmarkCircleOutline className={style['activity_icon']} />
                                <div>내가 참여한 피드</div>
                                <IoIosArrowForward className={style['activity_icon']} />

                                <HiOutlineBellAlert className={style['activity_icon']} />
                                <div>알림</div>
                                <IoIosArrowForward className={style['activity_icon']} />
                            </div>
                        </div>
                    </div>
                </>
            }

            {
                isClicked &&
                <>
                    <div className={`${style['base_box']} ${style['height_auto']}`}>
                        <h4>개인 정보</h4>
                        <div className={style['personal_info']}>
                            <div className={style['info_list']}>
                                <div className={style['info_items']}>UID</div>
                                <div className={style['info_items']}>{myData.uid}</div>

                                <div className={style['info_items']}>Email</div>
                                <div className={style['info_items']}>{myData.email}</div>

                                <div className={style['info_items']}>나이</div>
                                <div className={style['info_items']}>{myData.age}</div>

                                <div className={style['info_items']}>성별</div>
                                <div className={style['info_items']}>{myData.gender}</div>

                                <div className={style['info_items']}>별별 티켓 보유량</div>
                                <div className={style['info_items']}>{myData.credit}개</div>

                                <div className={style['info_items']}>우주인 패스</div>
                                <div className={style['info_items']}>미등록</div>
                            </div>
                        </div>
                    </div>
                    <div className={`${style['base_box']} ${style['height_auto']}`}>
                        <h4>닉네임</h4>
                    </div>
                    <div className={`${style['base_box']} ${style['height_auto']}`}>
                        <h4>활동 배지</h4>
                    </div>
                </>
            }
        </div>
    )
}

export default MyPage;