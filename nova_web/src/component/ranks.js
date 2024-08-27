import icon from '../img/Icon.png';
import star from '../img/star.png';
import { useNavigate } from 'react-router-dom';

function Ranks({ rank, isClicked }) {

    let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    let navigate = useNavigate();

    return (
        <div className="league" >
            {
                rank.map(function (a, i) {
                    {
                        return (
                            <div className="rank-item-box" key={i}>
                                <p className='rank-num'>{i+1}</p>
                                <div className='star'>
                                    <img src={star}/>
                                </div>
                                <div className="rank-profile">
                                    <img src={profile_url + `${rank[i].bid}.PNG`}></img>
                                </div>
                                <div className="name" onClick={()=>{
                                    navigate(`/bias_info/user_contribution?bias_id=${rank[i].bid}`)
                                }}>{rank[i].bname}</div>
                                <div className="point">{rank[i].point}pt
                                    <img src={icon} alt='next'></img>
                                </div>
                            </div>
                        )
                    }
                })
            }
        </div>
    )
}

export default Ranks;