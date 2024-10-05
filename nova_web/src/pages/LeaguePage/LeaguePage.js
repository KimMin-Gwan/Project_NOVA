import style from './LeaguePage.module.css';
import planetStyle from './../PlanetPage/Planet.module.css';
import icon from '../../img/Icon.png';
import star from '../../img/star.png';
import ThreeScene from '../../component/3Dimage';
import { useEffect, useRef, useState } from 'react';

export default function LeaguePage() {

    let [leagueData, setLeagueData] = useState([]);
    let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';
    let [loading, setLoading] = useState(true);

    useEffect(() => {
        const newSocket = new WebSocket('wss://nova-platform.kr/league_detail/league_data?league_name=고양이 은하');
        //const newSocket = new WebSocket('ws://127.0.0.1:4000/league_detail/league_data?league_name=고양이 은하');
        //wsRef.current = new WebSocket('ws://127.0.0.1:4000/league_detail/league_data?league_name=고양이 은하');

        newSocket.onopen = () => {
            console.log('Connected to the server')
        }

        //newSocket.onmessage = (event) => {
            //const message = event.data;
            //setMessages((pre))
        //}

        newSocket.onmessage = (event) => {
            console.log('Message from server:', event.data);
            const receiveData = event.data;
            console.log('dsad', receiveData);
            const splitData = receiveData.split(' ');
            const realData = splitData.map(part => part.split('.'));
            setLeagueData(realData)
            setLoading(false)
            newSocket.send("ack") //이걸 적으면 정상동작하게됨 ㅋㅋ
        };
        newSocket.addEventListener('error', (error) => {
            console.error('WebSocket error:', error);
        });
        newSocket.onclose = () => {
            console.log('close socket');
        };

        //setSocket(newSocket);

        return () => {
            //wsRef.current.close();
            newSocket.close();
        }
    }, [])

    // console.log(leagueData)

    // rank, bid, bname, point

    return (
        <div className={style.container}>
            <div className={style.title}>은하리그 페이지</div>
            <div className={style.imgArea}>
                <ThreeScene></ThreeScene>
            </div>
            <div className={style.league}>
                {
                    leagueData.map((data, i) => {
                        if (data[0] !== '/') {
                            return (
                                <div className="rank-item-box" key={i}>
                                    <p className='rank-num'>{data[0]}</p>
                                    <div className='star'>
                                        <img src={star} />
                                    </div>
                                    <div className="rank-profile">
                                        <img src={profile_url + `${data[1]}.PNG`}></img>
                                    </div>
                                    <div className="name">{data[2]}</div>
                                    <div className="point">{data[3]} pt
                                        <img src={icon} alt='next'></img>
                                    </div>
                                </div>
                            )
                        }
                        if (loading) {
                            <div>loading</div>
                        }
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