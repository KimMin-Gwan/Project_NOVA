import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import style from './Planet.module.css';

import LeagueCard from '../../component/LeagueCard';

import planet_img1 from './../../img/card_planet.png';
import planet_img2 from './../../img/planet2.png';
import planet_img3 from './../../img/planet3.png';
import planet_img4 from './../../img/station.png';


export default function PlanetList() {

    let [planets, setPlanets] = useState([]);
    let imgs = [planet_img1, planet_img2, planet_img3, planet_img4];

    let navigate = useNavigate();

    useEffect(() => {
        fetch('https://nova-platform.kr/feed_explore/feed_meta_data')
            .then(response => response.json())
            .then(data => {
                setPlanets(data.body.feed_meta_data);
            })
    }, [])

    // function handleClick() {
    //     navigate(`/feed_page?fclass=${planets.fclass}`);
    // };

    return (
        <div className={`container ${style.feedpage}`}>
            <div className={style['top_area']}>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>행성 탐색</div>
            </div>

            {
                planets.map((planet, i) => {
                    return (
                        <div key={i} onClick={() => {
                            navigate(`/feed_page?fclass=${planet.fclass}`);
                        }}>
                            <LeagueCard img={imgs[i]} name={planet.fname} info={planet.specific} type='planet'></LeagueCard>
                        </div>
                    )
                })

            }

            <div className={`${style['league_card']} ${style['rule_box']}`}>
                <h2>은하 리그 규칙</h2>
                <h4>로그인 후 사용 가능한 컨텐츠입니다.</h4>
                <h4>타인에게 불편을 줄 수 있는 내용의 게시글은 경고없이 삭제될 수 있습니다.</h4>
                <h4>본 게시글은 인공지능 프로그램에 의해 검열 및 관리되고 있습니다.</h4>
                <h4 className={style['last_rule']}>홍보와 관련된 내용은 우주 펀딩 페이지를 사용해주세요.</h4>
            </div>
            <div style={{ height: '10px', paddingBottom: '5px' }}></div>
        </div>
    )
}

