import plus from '../../img/plus.png';
import empty from '../../img/empty.png';
import more from '../../img/more.png';
import shadow from '../../img/shadow.png';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import SelectBias from '../selectBias/SelectBias';


function MySoloBias({ solo_bias, bias_url, showBox, blackBox }) {

    let [selectWindow, setSelectWindow] = useState(false);
    let navigate = useNavigate();

    function showSelectModal() {
        setSelectWindow(!selectWindow);
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
            // 'token': token,
            'type': 'solo'
        }
    }

    let url = 'https://nova-platform.kr/';
    let [bias_data, setBiasData] = useState();
    // useEffect(() => {
    //     fetch(url + `nova_check/server_info/check_page`, {
    //         method: 'post',
    //         headers: {
    //             "Content-Type": 'application/json',
    //         },
    //         body: JSON.stringify(send_data),
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             JSON.stringify(data)
    //         })
    // }, [])




    return (
        <div className='left-box'>
            {/* {
                 (
                    <>
                        <img src={empty} alt=''></img>
                        <div className='box'>
                            <div className='my-bias-group'>새로운 최애 솔로<br />지지하기</div>
                        </div>
                        <div className='more' onClick={() => {
                            alert('로그인을 해주세요.')
                        }}>
                            <img src={plus} alt=''></img>
                        </div>
                    </>
                )
            } */}
            {solo_bias.bid === '' && (
                <>
                    <img src={empty} alt='' onClick={() => {
                        showSelectModal();
                    }}></img>
                    <div className='box'>
                        <div className='my-bias-group'>새로운 최애 솔로<br />지지하기</div>
                    </div>

                    {
                        !selectWindow && <div className='more' onClick={() => {
                            showSelectModal();
                        }}>
                            <img src={plus} alt=''></img>
                        </div>
                    }
                    {
                        selectWindow && <SelectBias selectWindow={selectWindow} setSelectWindow={setSelectWindow}></SelectBias>
                    }


                </>
            )}
            {solo_bias.bid && (
                <>
                    <div className='image-container'>
                        <img src={bias_url + `${solo_bias.bid}.PNG`} alt="bias" className='img2' />
                    </div>
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
                                bias: bias_data.bias, result: bias_data.result, point: bias_data.point,
                                specialTime: bias_data.special_time
                            }
                        })
                    }} >지지하기</div>
                    <div className='box'>
                        <div className='my-bias-solo'>나의 최애</div>
                        <div className='bias-name' onClick={() => {
                            navigate(`/bias_info/user_contribution?bias_id=${solo_bias.bid}`)
                        }}>{solo_bias.bname}</div>
                    </div>
                    <div className='more' onClick={() => {
                        navigate(`/bias_info/user_contribution?bias_id=${solo_bias.bid}`)
                    }}>
                        <img src={more} alt=''></img>
                    </div>
                </>
            )}
        </div>
    )
}

export default MySoloBias;
