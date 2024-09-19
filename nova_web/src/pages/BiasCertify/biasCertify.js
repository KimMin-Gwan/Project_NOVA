import { useLocation, useNavigate } from 'react-router-dom';
import style from './biasCertify.module.css';
import bias from './../../img/bias.png';
import bias_back from './../../img/bias_back.png';
import circle from './../../img/circle.png';
import ProgressBar from './ProgressBar';
import { useState } from 'react';

function BiasCertify() {

    const currentTime = new Date().getHours();
    let navigate = useNavigate();
    let location = useLocation();
    let { token, bias, result, point, specialTime } = location.state || {};

    let url = 'https://nova-platform.kr/nova_check/server_info/';

    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/user_system/",
    }

    let send_data = {
        "header": header,
        "body": {
            'token': token,
            'type': bias.type
        }
    }

    let [checkResult, setCheckResult] = useState(result);
    let [checkSpecialTime, setSpecialTime] = useState()

    if (
        checkResult === 'valid'
    ) {
        return (
            <div className={`container ${style['main-container']}`}>
                <div className={`white-title ${style['title-area']}`}>
                    <button onClick={() => {
                        navigate(-1)
                    }}>뒤로</button>
                    <div>나의 최애 지지하기</div>
                </div>
                <div className={style['certify-container']}>
                    <div className={style['point-area']}>
                        <div className={style['save-point-box']}>
                            <div className={style.point}>
                                <div>누적 적립 포인트 : {point}</div>
                                <div>80%</div>
                            </div>
                            <ProgressBar />
                            {/* <div className={style['progress-container']}>
                            <div className={style['progress-bar']}></div>
                        </div> */}
                            {/* <progress value={50} min={0} max={100}>22</progress> */}
                        </div>
                    </div>
                    <div className={style.area}>
                        <div className={style['bias-area']}>
                            <div className={style['name-area']}>이름영역 : {bias.bname}</div>
                            <div className={style['img-area']}>
                                <div className={style.circle}>
                                    <img src={circle}></img>
                                    {/* <div>
                                    <img src={`https://kr.object.ncloudstorage.com/nova-images/${bias.bid}.PNG`}/>
                                </div> */}
                                </div>
                            </div>
                            <div className={style['bottom-area']}>
                                <div className={style['text-area']}>최애 인증하고 '{bias.nickname.length == 0 ? bias.bname : bias.nickname[0]}'을(를) 응원해요!</div>
                                <div className={style['button-area']}>
                                    {
                                        result === 'valid' && <div className={style.buttons} onClick={() => {
                                            fetch(url + 'try_daily_check', {
                                                method: 'post',
                                                headers: {
                                                    "Content-Type": 'application/json',
                                                },
                                                body: JSON.stringify(send_data),
                                            })
                                                .then(response => response.json())
                                                .then(data => {
                                                    // JSON.stringify(data)
                                                    console.log(data.body)
                                                    setCheckResult(data.body.result);
                                                });
                                        }}>인증 하기</div>
                                    }
                                    {/* {
                                        result === 'done' && <div className={style.buttons}>특별 인증</div>
                                    } */}
                                    {
                                        result === 'invalid' || result === 'error' && alert('잘못된 접근입니다.')
                                    }
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
    else if (checkResult === 'daily done') {
        return (
            <div className={`container ${style['main-container']}`}>
                <div className={`white-title ${style['title-area']}`}>
                    <button onClick={() => {
                        navigate(-1)
                    }}>뒤로</button>
                    <div>나의 최애 지지하기</div>
                </div>
                <div className={style['certify-container']}>
                    <div className={style['point-area']}>
                        <div className={style['save-point-box']}>
                            <div className={style.point}>
                                <div>누적 적립 포인트 : {point}</div>
                                <div>80%</div>
                            </div>
                            <ProgressBar />
                            {/* <div className={style['progress-container']}>
                            <div className={style['progress-bar']}></div>
                        </div> */}
                            {/* <progress value={50} min={0} max={100}>22</progress> */}
                        </div>
                    </div>
                    <div className={style.area}>
                        <div className={style['bias-area']}>
                            <div className={style['name-area']}>이름영역 : {bias.bname}</div>
                            <div className={style['img-area']}>
                                <div className={style.circle}>
                                    <img src={circle}></img>
                                    {/* <div>
                                    <img src={`https://kr.object.ncloudstorage.com/nova-images/${bias.bid}.PNG`}/>
                                </div> */}
                                </div>
                            </div>
                            <div className={style['bottom-area']}>
                                <div className={style['text-area']}>최애 인증하고 '{bias.nickname === '' ? bias.bname : bias.nickname[0]}'을(를) 응원해요!</div>
                                <div className={style['button-area']}>
                                    {/* {
                                        result === 'valid' && <div className={style.buttons} onClick={() => {
                                            fetch(url, {
                                                method: 'post',
                                                headers: {
                                                    "Content-Type": 'application/json',
                                                },
                                                body: JSON.stringify(send_data),
                                            })
                                                .then(response => response.json())
                                                .then(data => {
                                                    // JSON.stringify(data)
                                                    console.log(data.body)
                                                    setCheckResult(data.body.result);
                                                });
                                        }}>인증 하기</div>
                                    } */}
                                    {
                                        checkSpecialTime !== 'special done' &&
                                        <div className={style.buttons} onClick={() => {
                                            specialTime.includes(currentTime) ? alert('특별 인증이 완료되었습니다.')
                                                : alert('특별시가 아닙니다.')
                                            fetch(url + 'try_special_check', {
                                                method: 'post',
                                                headers: {
                                                    "Content-Type": 'application/json',
                                                },
                                                body: JSON.stringify(send_data),
                                            })
                                                .then(response => response.json())
                                                .then(data => {
                                                    // JSON.stringify(data)
                                                    console.log(data)
                                                    setSpecialTime(data.body.result);
                                                    console.log(specialTime)
                                                });

                                        }}>특별 인증</div>
                                        //time imvalid alert창 지금은 시간이 아님
                                    }
                                    {/* {
                                        specialTime.includes(currentTime) ? alert('특별 인증이 완료되었습니다.')
                                            : alert('특별시가 아닙니다.')
                                    } */}
                                    {
                                        result === 'invalid' || result === 'error' && alert('잘못된 접근입니다.')
                                    }
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
    else {
        return (<div>ddd</div>
        )
    }
}

export default BiasCertify;