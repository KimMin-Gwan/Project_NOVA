import { Routes, Route, Link } from 'react-router-dom'
import Loundspeaker from '../../component/loundspeaker';
import style from './Mypage.module.css';
function MyPage() {


    return (
        <div className={`container ${style['main-container']}`}>
            <div className={`white-title ${style['title-area']}`}>마이페이지</div>
            <div className={style['bias-show-area']}>
                <div className={style['bias-box']}>개인</div>
                <div className={style['bias-box']}>단체</div>
            </div>
            <div className={style['my-info-area']}>
                <div className={style['my-info']}>UID</div>
            </div>

            <div className={style['sub-info-area']}>
                <div className={style['sub-info']}>
                    <div className={style.info}>명함</div>
                </div>
                <div className={style['market-button']}>
                    <div className={style.market}>상점 바로가기</div>
                </div>
            </div>
        </div>
        // <Loundspeaker></Loundspeaker>
        // <div>dd</div>
        // <Link to='/' className='button'>홈</Link>
    )
}

export default MyPage;