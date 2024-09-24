import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import style from './Mypage.module.css';
import { SlSpeech } from "react-icons/sl";
import { HiOutlineBellAlert } from "react-icons/hi2";
import { IoIosArrowForward, IoIosArrowBack } from "react-icons/io";
// import MySoloBias from '../../component/subscribeBias/mySoloBias';
function MyPage() {

    let bias_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    let navigate = useNavigate();

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
                            <div><IoIosArrowForward />
                                <IoIosArrowBack /></div>
                        </div>
                    </div>
                    <div className={style['ticket_part']}>
                        <div className={style['ticket_info']}>
                            <div>별별티켓</div>
                            <div>640개</div>
                        </div>
                        <div className={style['btn_container']}>
                            <button>충전</button>
                            <button>패스</button>
                        </div>
                    </div>
                </div>
            </div>

            <div className={style['base_box']}>
                <h4>최애-개인</h4>
                <div className={style['wrap_box']} style={{ flexDirection: 'row', height: 'auto' }}>
                    <div className={style['half_box']}>
                        <div className={`left-box ${style['img_box']}`}>
                            <div className='image-container'>
                                <img src={bias_url + `1001.PNG`} alt="bias" className='img2' />
                            </div>
                        </div>
                    </div>
                    <div className={style['half_box']}>
                        <div className={style['text_box']}>
                            <p>나의최애</p>
                            <div className={style['bias_name']}>이시연</div>
                            <div>이번 시즌에 기여한 별가루</div>
                            <div>1200 pt</div>
                            <button>펀딩</button>
                        </div>
                    </div>
                </div>

            </div>


            <div className={style['base_box']}>
                <h4>최애-단체</h4>
                <div className={style['wrap_box']} style={{ flexDirection: 'row', height: 'auto' }}>
                    <div className={style['half_box']}>
                        <div className={`left-box ${style['img_box']}`}>
                            <div className='image-container'>
                                <img src={bias_url + `1001.PNG`} alt="bias" className='img2' />
                            </div>
                        </div>
                    </div>
                    <div className={style['half_box']}>
                        <div>나의최애</div>
                        <div>이시연</div>
                        <div>이번 시즌에 기여한 별가루</div>
                        <div>1200 pt</div>
                        <button>펀딩</button>
                    </div>
                </div>
            </div>


            <div className={`${style['base_box']} ${style['height_auto']}`}>
                <h4>서비스</h4>
                <div className={style['grid_container']}>
                    <div>은하리그</div>
                    <div>노바 펀딩</div>
                    <div>노바 재판</div>
                </div>

            </div>
            <div className={`${style['base_box']} ${style['height_auto']}`}>
                <h4>나의 활동</h4>
                <div className={style['my_activity']}>
                    <div className={style.activity}>
                        <SlSpeech className={style['activity_icon']} />
                        <div>내가 작성한 피드</div>
                        <IoIosArrowForward className={style['activity_icon']} />

                        <HiOutlineBellAlert className={style['activity_icon']} />
                        <div>알림</div>
                        <IoIosArrowForward className={style['activity_icon']} />

                        <HiOutlineBellAlert className={style['activity_icon']} />
                        <div>알림</div>
                        <IoIosArrowForward className={style['activity_icon']} />
                    </div>
                </div>
            </div>

            <div className={`${style['base_box']} ${style['height_auto']}`}>
                <h4>개인 정보</h4>
                <div className={style['personal_info']}>
                    <div className={style['info_list']}>
                        <div className={style['info_items']}>UID</div>
                        <div className={style['info_items']}>1234-abcd-5678</div>

                        <div className={style['info_items']}>Email</div>
                        <div className={style['info_items']}>sample123@email.com</div>

                        <div className={style['info_items']}>나이</div>
                        <div className={style['info_items']}>24살</div>

                        <div className={style['info_items']}>성별</div>
                        <div className={style['info_items']}>남성</div>

                        <div className={style['info_items']}>별별 티켓 보유량</div>
                        <div className={style['info_items']}>120개</div>

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


        </div>
    )
}

export default MyPage;