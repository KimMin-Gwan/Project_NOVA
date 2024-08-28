import plus from '../../img/plus.png';
import empty from '../../img/empty.png';
import more from '../../img/more.png';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function MyGroupBias({ group_bias, bias_url, token }) {

    let navigate = useNavigate();

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
            'type': 'group'
        }
    }

    let url = 'http://nova-platform.kr/';
    let [bias_data, setBiasData] = useState();

    return (
        <div className='left-box'>
            {
                (token === '' || !token) && (
                    <>
                        <img src={empty}></img>
                        <div className='box'>
                            <div className='my-bias-group'>새로운 최애 그룹<br />지지하기</div>
                        </div>
                        <div className='more' onClick={() => {
                            alert('로그인을 해주세요.')
                        }}>
                            <img src={plus}></img>
                        </div>
                    </>
                )
            }
            {group_bias.bid === '' && (
                <>
                    <img src={empty}></img>
                    <div className='box'>
                        <div className='my-bias-group'>새로운 최애 그룹<br />지지하기</div>
                    </div>
                    <div className='more' onClick={() => {
                        navigate('/select_bias')
                    }}>
                        <img src={plus}></img>
                    </div>
                </>
            )}
            {group_bias.bid && (
                <>
                    <img src={bias_url + `${group_bias.bid}.PNG`}></img>
                    <div className='support' onClick={() => {
                        fetch(url + `nova_check/server_info/check_page`, {
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
                                setBiasData(data.body)
                            });
                        navigate(`/bias_certify`, {
                            state: {
                                token: token, bias: bias_data.bias, result: bias_data.result, point: bias_data.point,
                                specialTime: bias_data.special_time
                            }
                        })
                    }} >지지하기</div>
                    <div className='box'>
                        <div className='my-bias-solo'>최애 그룹</div>
                        <div className='bias-name' onClick={() => {
                            navigate(`/bias_info/user_contribution?bias_id=${group_bias.bid}`)
                        }}>{group_bias.bname}</div>
                    </div>
                    <div className='more' onClick={() => {
                        navigate(`/bias_info/user_contribution?bias_id=${group_bias.bid}`)
                    }}>
                        <img src={more}></img>
                    </div>
                </>
            )}
        </div>
    )
}

export default MyGroupBias;