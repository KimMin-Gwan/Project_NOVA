import { useNavigate } from "react-router-dom";
import Ranks from "../../component/ranks";
import icon from '../../img/Icon.png';
import star from '../../img/star.png';
import style from './LeagueDetail.module.css'


export default function LeagueDetail() {
    const array = [1, 2, 3, 4, 5];
    let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    let navigate = useNavigate();

    return (
        <div className={style.container}>
            <div className={style.title}>리그 상세 페이지</div>
            <div className={style.league} >
                {
                    array.map((a, i) => {
                        return (
                            <div className="rank-item-box" key={i}>
                                <p className='rank-num'>{i}</p>
                                <div className='star'>
                                    <img src={star} />
                                </div>
                                <div className="rank-profile">
                                    {i}
                                    {/* <img src={profile_url + `${rank[i].bid}.PNG`}></img> */}
                                </div>
                                <div className="name">name</div>
                                <div className="point">{i} pt
                                    <img src={icon} alt='next'></img>
                                </div>
                            </div>
                        )
                    })
                }

            </div>
        </div>
    )
}