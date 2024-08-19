import plus from '../../img/plus.png';
import empty from '../../img/empty.png';
import more from '../../img/more.png';

function MyGroupBias({ group_bias, bias_url }) {

    return (
        <div className='left-box'>
            {group_bias.bid === '' && (
                <>
                    <img src={empty}></img>
                    <div className='box'>
                        <div className='my-bias-group'>새로운 최애 그룹<br />지지하기</div>
                    </div>
                    <div className='more'>
                        <img src={plus}></img>
                    </div>
                </>
            )}
            {group_bias.bid && (
                <>
                    <img src={bias_url + `${group_bias.bid}.PNG`}></img>
                    <div className='support'>지지하기</div>
                    <div className='box'>
                        <div className='my-bias-solo'>최애 그룹</div>
                        <div className='bias-name'>{group_bias.bname}</div>
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