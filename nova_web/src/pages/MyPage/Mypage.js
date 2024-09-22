import { Routes, Route, Link } from 'react-router-dom'
import style from './Mypage.module.css';
import MySoloBias from '../../component/subscribeBias/mySoloBias';
function MyPage() {


    return (
        <div className={`container ${style['main-container']}`}>
            <div className={`white-title ${style['title-area']}`}>마이페이지</div>
            <div className={style['bias-show-area']}>
                <div className={style['personal_box']}>
                    <div className={style['personal_area']}>
                        <div className={style.personal}>
                            <div>지지자</div>
                            <div>우주인 패스 +</div>
                            <div>화살표</div>
                        </div>
                    </div>

                    <div className={style['ticket_info']}></div>
                </div>
            </div>
            <div className={style['my-info-area']}>
                <div className={style['my-info']}>
                    <div className={style['info-box']}>
                        <div>UID</div>
                        <div>1234-1232-4564</div>
                    </div>
                    <div className={style['info-box']}>
                        <div>Email</div>
                        <div>sample123@gmail.com</div>
                    </div>
                    <div className={style['info-box']}>
                        <div>나이</div>
                        <div>24살</div>
                    </div>
                    <div className={style['info-box']}>
                        <div>성별</div>
                        <div>1234-1232-4564</div>
                    </div>

                </div>
            </div>

            <div className={style['sub-info-area']}>
                <div className={style['sub-info']}>
                    <div className={style.info}>명함</div>
                </div>
                <div className={style['market-button']}>
                    <div className={style.market}>상점 바로가기</div>
                    <Link to='/' className='button'>홈</Link>
                </div>
            </div>
        </div>
        // <Loundspeaker></Loundspeaker>
    )
}

export default MyPage;