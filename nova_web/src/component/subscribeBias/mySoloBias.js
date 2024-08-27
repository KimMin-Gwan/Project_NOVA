import plus from '../../img/plus.png';
import empty from '../../img/empty.png';
import more from '../../img/more.png';
import shadow from '../../img/shadow.png';
import { Routes, Route, Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';


function MySoloBias({ solo_bias, bias_url, token }) {

    let navigate = useNavigate();

    return (
        <div className='left-box'>
            {
                (token === '' || !token) && (
                    <>
                        <img src={empty} alt=''></img>
                        <div className='box'>
                            <div className='my-bias-group'>새로운 최애 솔로<br />지지하기</div>
                        </div>
                        <div className='more' onClick={() => {
                            navigate('mypage')
                        }}>
                            <img src={plus} alt=''></img>
                        </div>
                    </>
                )
            }
            {solo_bias.bid === '' && (
                <>
                    <img src={empty} alt=''></img>
                    <div className='box'>
                        <div className='my-bias-group'>새로운 최애 솔로<br />지지하기</div>
                    </div>
                    <div className='more' onClick={() => {
                        navigate('mypage')
                    }}>
                        <img src={plus} alt=''></img>
                    </div>
                </>
            )}
            {solo_bias.bid && (
                <>
                    <div className='image-container'>
                        <img src={bias_url + `${solo_bias.bid}.PNG`} alt="bias" className='img2' />
                    </div>
                    <div className='support' onClick={() => {
                        navigate(`/bias_certify`)
                    }} >지지하기</div>
                    <div className='box'>
                        <div className='my-bias-solo'>나의 최애</div>
                        <div className='bias-name' onClick={() => {
                            navigate(`/bias_info/user_contribution?bias_id=${solo_bias.bid}`)
                        }}>{solo_bias.bname}</div>
                    </div>
                    <div className='more' onClick={() => {
                        navigate(`/bias_certify`)
                    }}>
                        <img src={more} alt=''></img>
                    </div>
                </>
            )}
        </div>
    )
}

export default MySoloBias;
