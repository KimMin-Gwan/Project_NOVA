import { useNavigate } from 'react-router-dom';
import style from './biasCertify.module.css';

function BiasCertify() {

    let navigate = useNavigate();

    return (
        <div className={`container ${style['main-container']}`}>
            <div className={`white-title ${style['title-area']}`}>
                <button onClick={() => {
                    navigate(-1)
                }}>뒤로</button>
                <div>최애 인증하기</div>
            </div>
            <div className={style['certify-container']}>
                <div className={style.area}>
                    <div className={style['save-point-box']}>현재까지 적립한 포인트</div>
                </div>
                <div className={style.area}>
                    <div className={style.buttons}>최애인증</div>
                </div>
                <div className={style.area}>
                    <div className={style.buttons}>명함 보기</div>
                </div>
            </div>
            <div className={style.advise}>광고 영역</div>
        </div>
    )
}

export default BiasCertify;