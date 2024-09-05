import style from './LeaguePage.module.css';
import icon from '../../img/Icon.png';
import star from '../../img/star.png';
import ThreeScene from '../../component/3Dimage';

export default function LeaguePage() {

    const array = [1, 2, 3, 4, 5];

    return (
        <div className={style.container}>
            <div className={style.title}>리그 페이지</div>
            <div className={style.imgArea}>
                <ThreeScene></ThreeScene>
            </div>
            <div className={style.league}>
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