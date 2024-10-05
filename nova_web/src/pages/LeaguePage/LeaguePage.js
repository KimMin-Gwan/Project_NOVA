import style from './LeaguePage.module.css';
import planetStyle from './../PlanetPage/Planet.module.css';
import icon from '../../img/Icon.png';
import star from '../../img/star.png';
import ThreeScene from '../../component/3Dimage';

export default function LeaguePage() {

    const array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    function fetchLeagueData() {
        fetch('https://nova-platfomr.kr/league_detail/league_data', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                console.log('league_Data', data);
            });
    };

    return (
        <div className={style.container}>
            <div className={style.title}>은하리그 페이지</div>
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
            <div className={`${planetStyle['league_card']} ${planetStyle['rule_box']}`}>
                <h2>은하 리그 규칙</h2>
                <h4>1위를 한 최애는 홈 화면 피드에 등장하게 됩니다.</h4>
                <h4>1위를 한 최애의 지지자는 기여도에 따라 은하 티켓을 받게 됩니다.</h4>
                <h4>우주인 패스 등록 지지자는 최애가 1위를 하지 않아도 은하 티켓을 받습니다.</h4>
                <h4>리그는 14일 동안 진행됩니다.</h4>
                <h4>리그는 일요일 자정에 종료되며, 월요일 정오에 시작합니다.</h4>
                <h4 className={planetStyle['last_rule']}>지지자수의 변동과 획득 포인트에 따라 리그가 조정될 수 있습니다.</h4>
            </div>
        </div>
    )
}