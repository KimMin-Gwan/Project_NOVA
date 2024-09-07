import style from './../pages/PlanetPage/Planet.module.css';

export default function LeagueCard({img, name, info}) {

    return (
        <div className={style['league_card']}>
            <div className={style['img_area']}>
                <img src={img}></img>
            </div>
            <div className={style['planet_info']}>
                <h3>{name}</h3>
                <h5>{info}</h5>
            </div>
        </div>
    )
}