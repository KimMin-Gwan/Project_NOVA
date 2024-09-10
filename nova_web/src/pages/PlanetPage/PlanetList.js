import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import style from './Planet.module.css';

import LeagueCard from '../../component/LeagueCard';

import planet1 from './../../img/planet1.png';
import planet2 from './../../img/planet2.png';
import planet3 from './../../img/planet3.png';
import planet4 from './../../img/planet4.png';


export default function PlanetList() {

    let nameList = ['정거장 행성', '자랑 행성', '이지선다 행성', '퀴즈 행성'];
    let shortInfo = [
        '외부 링크 공유',
        '덕질 경험 자랑',
        '선택하라, 2가지 선택지 중에서',
        '함께 만들고 풀어보는 퀴즈'
    ]

    let navigate = useNavigate();

    function handleClick() {
        navigate('/feed_page');
    }


    return (
        <div className='container'>
            <div className={style['top_area']}>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>은하계 탐색</div>
            </div>
            {/* 정거정 행성 */}
            <div onClick={() => { navigate('/feed_page') }}>
                <LeagueCard img={planet1} name={nameList[0]} info={shortInfo[0]}></LeagueCard>
            </div>
            {/* 자랑 행성 */}
            <div onClick={() => { navigate('/feed_page') }}>
                <LeagueCard img={planet2} name={nameList[1]} info={shortInfo[1]}></LeagueCard>
            </div>
            {/* 이지선다 행성 */}
            <div onClick={() => { navigate('/feed_page') }}>
                <LeagueCard img={planet3} name={nameList[2]} info={shortInfo[2]}></LeagueCard>
            </div>
            {/* 퀴즈 행성 */}
            <div onClick={() => { navigate('/feed_page') }}>
                <LeagueCard img={planet4} name={nameList[3]} info={shortInfo[3]}></LeagueCard>
            </div>
            
            <div className={`${style['league_card']} ${style['rule_box']}`}>
                <h2>은하 리그 규칙</h2>
                <h4>로그인 후 사용 가능한 컨텐츠입니다.</h4>
                <h4>타인에게 불편을 줄 수 있는 내용의 게시글은 경고없이 삭제될 수 있습니다.</h4>
                <h4>본 게시글은 인공지능 프로그램에 의해 검열 및 관리되고 있습니다.</h4>
                <h4 className={style['last_rule']}>홍보와 관련된 내용은 우주 펀딩 페이지를 사용해주세요.</h4>
            </div>
        </div>
    )
}

