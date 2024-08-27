import plus from '../../img/plus.png';
import empty from '../../img/empty.png';
import more from '../../img/more.png';
import { useNavigate } from 'react-router-dom';


function MyGroupBias({ group_bias, bias_url, token }) {

    let navigate = useNavigate();

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
                            navigate('mypage')
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
                        navigate('mypage')
                    }}>
                        <img src={plus}></img>
                    </div>
                </>
            )}
            {group_bias.bid && (
                <>
                    <img src={bias_url + `${group_bias.bid}.PNG`}></img>
                    <div className='support' onClick={() => {
                        navigate(`/bias_info/user_contribution?bias_id=${group_bias.bid}`)
                    }}>지지하기</div>
                    <div className='box'>
                        <div className='my-bias-solo'>최애 그룹</div>
                        <div className='bias-name' onClick={() => {
                            navigate(`/bias_info/user_contribution?bias_id=${group_bias.bid}`)
                        }}>{group_bias.bname}</div>
                    </div>
                    <div className='more'>
                        <img src={more}></img>
                    </div>
                </>
            )}
        </div>
    )
}

export default MyGroupBias;