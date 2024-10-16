import { useLocation, useNavigate } from 'react-router-dom';
import style from './biasCertify.module.css';
import bias from './../../img/bias.png';
import bias_back from './../../img/bias_back.png';
import circle from './../../img/circle.png';
import ProgressBar from './ProgressBar';
import star from '../../img/star.png';

import { useEffect, useState } from 'react';
import backword from "./../../img/back_icon.png";


function BiasCertify() {

    const currentTime = new Date().getHours();
    let navigate = useNavigate();
    let location = useLocation();
    // let { bias, result, point, specialTime } = location.state || {};

    // console.log('dasdadasdad', bias)
    let url = 'https://nova-platform.kr/nova_check/server_info/';


    // let url = 'https://nova-platform.kr/';
    let [biasData, setBiasData] = useState();
    let [showNameCard, setShowNameCard] = useState(false);

    function handleNameCard() {
        setShowNameCard(true);
    };

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
            'type': 'solo'
        }
    }

    function fetchCheckPoint() {
        fetch(url + `check_page`, {
            method: 'post',
            headers: {
                "Content-Type": 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(send_data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('지지하기', data.body);
                setBiasData(data.body);
            });

        console.log('biasdata', biasData);
    };

    useEffect(() => {
        fetchCheckPoint();
    }, []);

    function fetchAuthenData() {
        fetch(url + 'try_daily_check', {
            method: 'POST',
            headers: {
                "Content-Type": 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(send_data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('인증했나', data.body);
                setBiasData(data.body)
                // setBiasData((prevData)=>[...prevData, result: data.body.result])
                // setCheckResult(data.body.result);
            });
        console.log('biasdata', biasData);

    };

    function fetchSpecialAuthenData() {
        if (biasData.special_check_valid) {
            fetch(url + 'try_special_check', {
                method: 'post',
                headers: {
                    "Content-Type": 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(send_data),
            })
                .then(response => response.json())
                .then(data => {
                    setBiasData(data.body)
                    // setBiasData((prevData) => ({ ...prevData, result: data.result }))
                    console.log('스페셜인증', data)
                });
        } else {
            alert('특별인증 시간이 아닙니다.');
        }
    };



    // let [checkResult, setCheckResult] = useState(result);
    let [checkSpecialTime, setSpecialTime] = useState()

    if (biasData === undefined) {
        return (
            <div>로딩중...</div>
        )
    }


    // if (biasData.result === 'valid') {
    return (
        <div className={`container ${style['main-container']}`}>
            <div className={`white-title ${style['title-area']}`}>
                <img
                    src={backword}
                    alt="Arrow"
                    className={style.backword}
                    onClick={() => {
                        navigate(-1);
                    }}
                />
                <div>나의 최애 지지하기</div>
            </div>
            <div className={style['certify-container']}>
                <div className={style['point-area']}>
                    <div className={style['save-point-box']}>
                        <div className={style.point}>
                            <div>누적 적립 포인트 : </div>
                            <div>{biasData.point}</div>
                        </div>
                        <ProgressBar point={biasData.contribution} />
                    </div>
                </div>
                <div className={style.area}>
                    {
                        biasData.result === 'special done' || showNameCard ? (
                            <div className={style['bias_card']}>
                                <img src={biasData.name_card_url} alt='bias_img'/>
                                {/* <div>bu</div> */}
                            </div>
                        ) : (
                            <div className={style['bias-area']}>
                                <div className={style['name-area']}>
                                    <div className={`star ${style['star_img']}`}>
                                        <img src={star} />
                                    </div>
                                    <div className={style['name_style']}>
                                        {biasData.bias.bname}
                                    </div>
                                    <div className={`star ${style['star_img']}`}>
                                        <img src={star} />
                                    </div>
                                </div>
                                <div className={style['img-area']}>
                                    <div className={style.circle}>
                                        <img src={circle} alt='circle'></img>
                                        <div className={style['bias_img']}>
                                            <img src={`https://kr.object.ncloudstorage.com/nova-images/${biasData.bias.bid}.PNG`} alt='bias_img'/>
                                        </div>
                                    </div>
                                </div>
                                <div className={style['bottom-area']}>
                                    <div className={style['text-area']}>최애 인증하고 '{biasData.bias.nickname.length === 0 ? biasData.bias.bname : biasData.bias.nickname[0]}'을(를) 응원해요!</div>
                                    <div className={style['button-area']}>
                                        {
                                            biasData.result === 'valid' &&
                                            <div className={style.buttons} onClick={() => {
                                                fetchAuthenData()
                                            }}>인증 하기</div>
                                        }
                                        {
                                            biasData.result === 'daily done' &&
                                            (
                                                <>
                                                    <div className={style.buttons}
                                                        onClick={fetchSpecialAuthenData}
                                                    >특별 인증</div>
                                                    <div className={style.buttons} onClick={handleNameCard}>명함 보기</div>
                                                </>
                                            )
                                        }
                                    </div>
                                </div>
                            </div>
                        )
                    }
                </div>
            </div>
            {
                 (biasData.result === 'special done' || showNameCard) && (
                    <div className={style['download-btn-area']}>
                        <button>다운로드</button>
                    </div>
                 )
            }
            <div className={style.advise}>광고 영역</div>
        </div>
    )
}
export default BiasCertify;