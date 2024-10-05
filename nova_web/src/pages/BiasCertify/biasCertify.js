import { useLocation, useNavigate } from 'react-router-dom';
import style from './biasCertify.module.css';
import bias from './../../img/bias.png';
import bias_back from './../../img/bias_back.png';
import circle from './../../img/circle.png';
import ProgressBar from './ProgressBar';
import { useEffect, useState } from 'react';

function BiasCertify() {

    const currentTime = new Date().getHours();
    let navigate = useNavigate();
    let location = useLocation();
    // let { bias, result, point, specialTime } = location.state || {};

    // console.log('dasdadasdad', bias)
    let url = 'https://nova-platform.kr/nova_check/server_info/';


    // let url = 'https://nova-platform.kr/';
    let [biasData, setBiasData] = useState();

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
                    console.log('스페셜인증', data)
                    setBiasData((prevData) => ({ ...prevData, result: data.result }))
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


    // if (biasData.result === 'daily done') {
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
                            <div>누적 적립 포인트 : </div>
                            <div>{biasData.point}</div>
                        </div>
                        <ProgressBar />
                    </div>
                </div>
                <div className={style.area}>
                    <div className={style['bias-area']}>
                        <div className={style['name-area']}>이름영역 : {biasData.bias.bname}</div>
                        <div className={style['img-area']}>
                            <div className={style.circle}>
                                <img src={circle}></img>
                                {/* <div>
                                    <img src={`https://kr.object.ncloudstorage.com/nova-images/${biasData.bias.bid}.PNG`}/>
                                </div> */}
                            </div>
                        </div>
                        <div className={style['bottom-area']}>
                            <div className={style['text-area']}>최애 인증하고 '{biasData.bias.nickname.length == 0 ? biasData.bias.bname : biasData.bias.nickname[0]}'을(를) 응원해요!</div>
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
                                            <div className={style.buttons}>명함 보기</div>
                                        </>
                                    )
                                }
                                {
                                    biasData.result === 'special done' && <div>21</div>
                                }
                                {
                                    // biasData.special_check_valid가 false면 alert창 잘못된 시간에 누르면
                                }
                                {/* {
                                    biasData.result === 'invalid' && alert('잘못된 접근')
                                } */}
                                {/* {
                                    result === 'invalid' || result === 'error' && alert('잘못된 접근입니다.')
                                } */}
                                {/* <div className={style.buttons}>명함 보기</div> */}
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
    // }
    //     else if (checkResult === 'daily done') {
    //         return (
    //             <div className={`container ${style['main-container']}`}>
    //                 <div className={`white-title ${style['title-area']}`}>
    //                     <button onClick={() => {
    //                         navigate(-1)
    //                     }}>뒤로</button>
    //                     <div>나의 최애 지지하기</div>
    //                 </div>
    //                 <div className={style['certify-container']}>
    //                     <div className={style['point-area']}>
    //                         <div className={style['save-point-box']}>
    //                             <div className={style.point}>
    //                                 <div>누적 적립 포인트 : {point}</div>
    //                                 <div>80%</div>
    //                             </div>
    //                             <ProgressBar />
    //                             {/* <div className={style['progress-container']}>
    //                             <div className={style['progress-bar']}></div>
    //                         </div> */}
    //                             {/* <progress value={50} min={0} max={100}>22</progress> */}
    //                         </div>
    //                     </div>
    //                     <div className={style.area}>
    //                         <div className={style['bias-area']}>
    //                             <div className={style['name-area']}>이름영역 : {bias.bname}</div>
    //                             <div className={style['img-area']}>
    //                                 <div className={style.circle}>
    //                                     <img src={circle}></img>
    //                                     {/* <div>
    //                                     <img src={`https://kr.object.ncloudstorage.com/nova-images/${bias.bid}.PNG`}/>
    //                                 </div> */}
    //                                 </div>
    //                             </div>
    //                             <div className={style['bottom-area']}>
    //                                 <div className={style['text-area']}>최애 인증하고 '{bias.nickname === '' ? bias.bname : bias.nickname[0]}'을(를) 응원해요!</div>
    //                                 <div className={style['button-area']}>
    //                                     {/* {
    //                                         result === 'valid' && <div className={style.buttons} onClick={() => {
    //                                             fetch(url, {
    //                                                 method: 'post',
    //                                                 headers: {
    //                                                     "Content-Type": 'application/json',
    //                                                 },
    //                                                 body: JSON.stringify(send_data),
    //                                             })
    //                                                 .then(response => response.json())
    //                                                 .then(data => {
    //                                                     // JSON.stringify(data)
    //                                                     console.log(data.body)
    //                                                     setCheckResult(data.body.result);
    //                                                 });
    //                                         }}>인증 하기</div>
    //                                     } */}
    //                                     {
    //                                         checkSpecialTime !== 'special done' &&
    //                                         <div className={style.buttons} onClick={() => {
    //                                             specialTime.includes(currentTime) ? alert('특별 인증이 완료되었습니다.')
    //                                                 : alert('특별시가 아닙니다.')
    //                                             fetch(url + 'try_special_check', {
    //                                                 method: 'post',
    //                                                 headers: {
    //                                                     "Content-Type": 'application/json',
    //                                                 },
    //                                                 body: JSON.stringify(send_data),
    //                                             })
    //                                                 .then(response => response.json())
    //                                                 .then(data => {
    //                                                     // JSON.stringify(data)
    //                                                     console.log(data)
    //                                                     setSpecialTime(data.body.result);
    //                                                     console.log(specialTime)
    //                                                 });

    //                                         }}>특별 인증</div>
    //                                         //time imvalid alert창 지금은 시간이 아님
    //                                     }
    //                                     {/* {
    //                                         specialTime.includes(currentTime) ? alert('특별 인증이 완료되었습니다.')
    //                                             : alert('특별시가 아닙니다.')
    //                                     } */}
    //                                     {
    //                                         result === 'invalid' || result === 'error' && alert('잘못된 접근입니다.')
    //                                     }
    //                                     <div className={style.buttons}>명함 보기</div>
    //                                 </div>
    //                             </div>
    //                             {/* <img className={style.back} src={bias_back}></img> */}
    //                             {/* <div>이름</div> */}
    //                             {/* <div className={style.circle}>
    //                             <img src={circle}></img>
    //                         </div> */}
    //                             {/* <div className={style['bottom-area']}>
    //                             <div>응원해요</div>
    //                         </div> */}
    //                         </div>
    //                     </div>
    //                 </div>
    //                 <div className={style.advise}>광고 영역</div>
    //             </div>
    //         )
    //     }
    //     else if (bias === undefined) {
    //         return (<div>loading</div>)
    //     }
    //     else {
    //         return (<div>ddd</div>
    //         )
    //     }
    // }
}
export default BiasCertify;