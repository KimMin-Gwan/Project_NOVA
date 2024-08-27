import { Routes, Route, Link } from 'react-router-dom'
import Loundspeaker from '../../component/loundspeaker';
import style from './Mypage.module.css';
function MyPage() {


    return (
        <div className={`container ${style['main-container']}`}>
            <div className={`white-title ${style['title-area']}`}>마이페이지</div>
            <div className={style['bias-show-area']}>
                <div className={style['bias-box']}>
                    <div className={style['type-area']}>개인</div>
                    <div className={style['img-box']}>사진</div>
                    <div className={style['bias-name']}>최애 이름</div>
                    <div className={style['point-box']}>포인트</div>
                </div>
                <div className={style['bias-box']}>
                    <div className={style['type-area']}>단체</div>
                    <div className={style['img-box']}>사진</div>
                    <div className={style['bias-name']}>최애 이름</div>
                    <div className={style['point-box']}>포인트</div>
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