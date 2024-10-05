import { useEffect, useState } from 'react';
import style from './../pages/PlanetPage/Planet.module.css';

export default function LeagueCard({ img, name, info, type }) {

    let [imgSize, setImgSize] = useState(null);

    function handleSize(){
        if( type==='galaxy')
        {
            setImgSize(style['galaxy_img']);
        }
    };

    useEffect(()=>{
        handleSize();
    },[]);


    return (
        <div className={style['league_card']}>
            <div className={`${style['img_area']}`}>
                <img src={img} className={`${style['planet_img']} ${imgSize}`}></img>
            </div>
            <div className={style['planet_info']}>
                <h3>{name}</h3>

                {type === 'planet' && <h5>{info}</h5>}
                {
                    type === 'galaxy' && (
                        <>
                            <h5>지지자 범위 : {info.tier}</h5>
                            <h5>참여 지지자 : {info.num_bias}</h5>
                        </>
                    )
                }
            </div>
        </div>
    )
}