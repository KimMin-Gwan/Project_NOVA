import { useNavigate } from 'react-router-dom';
import style from './biasCertify.module.css';
import bias from './../../img/bias.png';
import bias_back from './../../img/bias_back.png';
import circle from './../../img/circle.png';

function BiasCertify() {

    let navigate = useNavigate();

    return (
        <div className={`container ${style['main-container']}`}>
            <div className={`white-title ${style['title-area']}`}>
                <button onClick={() => {
                    navigate(-1)
                }}>뒤로</button>
                <div>나의 최애 인증하기</div>
            </div>
            <div className={style['certify-container']}>
                <div className={style['point-area']}>
                    <div className={style['save-point-box']}>
                        <div className='white-title'>누적 적립 포인트</div>
                        <div className={style['progress-container']}>
                            <div className={style['progress-bar']}></div>
                        </div>
                        {/* <progress value={50} min={0} max={100}>22</progress> */}
                    </div>
                </div>
                <div className={style.area}>
                    <div className={style['bias-area']}>
                        <div className={style['name-area']}>이름영역</div>
                        <div className={style['img-area']}>
                            <div className={style.circle}>
                                <img src={circle}></img>
                            </div>
                        </div>
                        <div className={style['bottom-area']}>
                            <div className={style['text-area']}>최애 인증하고 ' '을(를) 응원해요!</div>
                            <div className={style['button-area']}>
                                <div className={style.buttons}>최애인증</div>
                                <div className={style.buttons}>명함 보기</div>
                            </div>
                        </div>
                        {/* <img className={style.back} src={bias_back}></img> */}
                        {/* <div>이름</div> */}
                        {/* <div className={style.circle}>
                            <img src={circle}></img>
                        </div> */}
                        {/* <div className={style['bottom-area']}>
                            <div>응원해요</div>
                        </div> */}
                    </div>
                </div>
            </div>
            <div className={style.advise}>광고 영역</div>
        </div>
    )
}

export default BiasCertify;