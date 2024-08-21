import plus from '../../img/plus.png';
import empty from '../../img/empty.png';
import more from '../../img/more.png';
import shadow from '../../img/shadow.png';

function MySoloBias({ solo_bias, bias_url }) {

    return (
        <div className='left-box'>
            {solo_bias.bid === '' && (
                <>
                    <img src={empty} alt=''></img>
                    <div className='box'>
                        <div className='my-bias-group'>새로운 최애 솔로<br />지지하기</div>
                    </div>
                    <div className='more'>
                        <img src={plus} alt=''></img>
                    </div>
                </>
            )}
            {solo_bias.bid && (
                <>
                    <div className='image-container'>
                        <img src={bias_url + `${solo_bias.bid}.PNG`} alt="bias" className='img2' />
                    </div>
                    <div className='support'>지지하기</div>
                    <div className='box'>
                        <div className='my-bias-solo'>나의 최애</div>
                        <div className='bias-name'>{solo_bias.bname}</div>
                    </div>
                    <div className='more'>
                        <img src={more} alt=''></img>
                    </div>
                </>
            )}
        </div>
    )
}

export default MySoloBias;
