import { useLocation } from "react-router-dom";
import style from './biasDetail.module.css';
import { useEffect, useState } from "react";

function BiasDetail() {
    let location = useLocation();
    let queryParams = new URLSearchParams(location.search);
    let data = queryParams.get('bias_id');
    let [userCtb, setUserCtb] = useState([]);
    let [myCtb, setMyCtb] = useState([]);
    let [checkSupport, setCheckSupport] = useState(false);

    let [biasData, setBiasData] = useState({
        nickname: [],
        country: [],
        fanname: [],
        group: [],
    });

    let url = 'http://175.106.99.34/bias_info/';
    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }
    let sample = localStorage.getItem('jwtToken');

    let send_data = {
        "header": header,
        "body": {
            "token": sample,
            'bid': data,
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://175.106.99.34/bias_info/user_contribution?bias_id=${data}`);
                const result = await response.json();

                // userCtbCopy = result.body.user_contribution;
                setUserCtb(result.body.user_contribution);
                // console.log(result.body.user_contribution);
            } catch (error) {
                console.error('Error fetching data: ', error);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        fetch(url + 'my_contribution', {
            method: 'post',
            headers: {
                "Content-Type": 'application/json',
            },
            body: JSON.stringify(send_data),
        })
            .then(response => response.json())
            .then(result => {
                // console.log(result.body);
                setCheckSupport(result.body.result);
                setMyCtb(result.body.my_contribution);
            })
    }, []);

    useEffect(() => {
        fetch(url + `bias_n_league?bias_id=${data}`)
            .then(response => response.json())
            .then(result => {
                console.log(result.body.result);
                setBiasData(result.body.result);
            })
    }, [url])

    //리그명 lname
    //현재 등수 rank
    //합계 포인트 point
    //전체 지지수 num_user
    //참여한 지지자수 contributed-user
    //타입은 개인과 단체
    return (
        <div className={`container ${style['main-container']}`}>
            <div className={style["title-area"]}>Title</div>
            <div className={`league ${style['info-box']}`}>
                <div className={`white-title rank-item-box`}>이름 : {biasData.bname}</div>
                {
                    biasData.birthday ? <div className={`white-title rank-item-box`}>생일 : {biasData.birthday}</div>
                        : <></>
                }
                {
                    biasData.debut ? <div className={`white-title rank-item-box`}>데뷔날짜 : {biasData.debut}</div>
                        : <></>
                }
                {
                    biasData.nickname.length!==0 ? <div className={`white-title rank-item-box`}>별명 : {biasData.nickname.join(', ')}</div>
                        : <></>
                }
                {
                    biasData.country.length!==0 ? <div className={`white-title rank-item-box`}>국적 : {biasData.country.join(', ')}</div>
                        : <></>
                }
                {
                    biasData.group.length!==0 ? <div className={`white-title rank-item-box`}>그룹 : {biasData.group.join(', ')}</div>
                        : <></>
                }
                {
                    biasData.agency ? <div className={`white-title rank-item-box`}>소속사 : {biasData.agency}</div>
                        : <></>
                }
            </div>
            <div className={`league ${style['detail-area']}`}>
                <div className={`white-title rank-item-box`}>리그명(범위) : {biasData.lname}</div>
                <div className={`white-title rank-item-box`}>현재등수 : {biasData.rank}</div>
                <div className={`white-title rank-item-box`}>합계 획득 포인트(이번시즌) : {biasData.point}</div>
                <div className={`white-title rank-item-box`}>전체 지지자 수 : {biasData.num_user}</div>
                <div className={`white-title rank-item-box`}>이번 시즌 참여 지지자 수 : {biasData.contributed_user}</div>
            </div>
            <div className={`white-title league ${style['my-support']}`}>
                나의 지지 상태
                {
                    checkSupport ? (
                        <div className="white-title rank-item-box">
                            <p className='rank-num'>{myCtb.rank}</p>
                            <div className="name">{myCtb.uid}</div>
                            <div className="point">{myCtb.point}pt</div>
                        </div>
                    )
                        : <></>
                }
            </div>
            <div className="league">
                {
                    userCtb.map(function (user, i) {
                        // console.log(user)
                        return (
                            <div className="rank-item-box" key={i}>
                                <p className='rank-num'>{user.rank}</p>
                                <div className="name">{user.uid}</div>
                                <div className="point">{user.point}pt</div>
                            </div>
                        )
                    })
                }
                {/* <div className="rank-item-box">
                    <p className='rank-num'>{1}</p>
                    <div className='star'>
                        <img src={star} />
                    </div>
                    <div className="rank-profile">
                        <img src={profile_url + `${rank[i].bid}.PNG`}></img>
                    </div>
                    <div className="name">{data}</div>
                    <div className="point">포인트pt</div>
                </div> */}
            </div>
        </div>
    )
}

export default BiasDetail;