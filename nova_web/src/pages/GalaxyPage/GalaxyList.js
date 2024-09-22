import { useNavigate } from 'react-router-dom';

import style from './../PlanetPage/Planet.module.css';
import LeagueCard from '../../component/LeagueCard';

import galaxy1 from './../../img/galaxy1.png';
import galaxy2 from './../../img/galaxy2.png';


export default function GalaxyList() {

    let galaxyName = ['고양이 은하 리그', '파란 고양이 은하 리그'];

    let navigate = useNavigate();

    function handleClick() {
        navigate('/league_detail');
    };

    return (
        <div className={`container ${style.feedpage}`}>
            <div className={style['top_area']}>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>은하계 탐색</div>
            </div>

            <div onClick={handleClick}>
                <LeagueCard img={galaxy1} name={galaxyName[0]} info='gkgk' type='galaxy'></LeagueCard>
            </div>
            <div onClick={handleClick}>
                <LeagueCard img={galaxy2} name={galaxyName[1]} info='gkgk' type='galaxy'></LeagueCard>
            </div>
            <div onClick={handleClick}>
                <LeagueCard img={galaxy2} name={galaxyName[1]} info='gkgk' type='galaxy'></LeagueCard>
            </div>

            <div className={`${style['league_card']} ${style['rule_box']}`}>
                <h2>은하 리그 규칙</h2>
                <h4>최애 인증을 통해 은하 리그에 참여하세요.</h4>
                <h4>1위를 한 최애는 홈 화면 피드에 등장하게 됩니다.</h4>
                <h4>1위를 한 최애의 지지자는 기여도에 따라 별별 티켓을 받게 됩니다.</h4>
                <h4>리그는 14일 동안 진행됩니다.</h4>
                <h4>리그는 일요일 자정에 종료되며, 월요일 정오에 시작합니다.</h4>
                <h4 className={style['last_rule']}>지지자수의 변동과 획득 포인트에 따라 리그가 조정될 수 있습니다.</h4>
            </div>
            <div style={{height:'10px', paddingBottom:'5px'}}></div>
        </div>
    )
}