import { useState, useEffect } from "react";
import League from "../component/league";

function Meta({ url, isSoloClicked, isGroupClicked, type, token }) {

    let [leagues, setLeagues] = useState([]);
    let league_copy = [];

    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }
    // let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyNDA0MDA1MCwiZXhwIjoxNzI0MDQxODUwfQ.WxZ9UAhZlD0hkNcyvc4rPN_IIraVr2oZSXvTuTteaQU'
    let sample = localStorage.getItem('jwtToken');

    let my_solo_league_copy = [];
    let my_group_league_copy = [];
    let [mySoloBiasLeague, setMySoloBiasLeague] = useState([]);
    let [myGroupBiasLeague, setMyGroupBiasLeague] = useState([]);

    // let send_data = {
    //     "header": header,
    //     "body": {
    //         'token': sample,
    //         'type': type,
    //     }
    // }
    useEffect(() => {
        {
            if (!token) {
                console.log('로그인 안됨')
            }
            else {
                const fetchData = async () => {
                    const response = await fetch(url + 'my_bias_league',
                        {
                            method: 'post',
                            headers: {
                                "Content-Type": 'application/json',
                            },
                            body: JSON.stringify({
                                "header": header,
                                "body": {
                                    'token': token,
                                    'type': type,
                                }
                            }),
                        }
                    );
                    const data = await response.json();
                    if (type === 'solo') {
                        my_solo_league_copy = [data.body.league_data.lname];
                        setMySoloBiasLeague(my_solo_league_copy);
                        console.log('solodata: ', mySoloBiasLeague);
                    }
                    if (type === 'group') {
                        my_group_league_copy = [data.body.league_data.lname];
                        setMyGroupBiasLeague(my_group_league_copy);
                        console.log('group : ', myGroupBiasLeague);
                    }
                };

                fetchData();
            }
        }
    }, [url, isGroupClicked, token])

    useEffect(() => {
        fetch(url + `league_data?league_type=${type}`)
            .then(response => response.json())
            .then(data => {
                setLeagues(data.body.leagues.map(leagues => leagues.lname));
            })
    }, [url])

    if (isSoloClicked) {
        {
            if ((mySoloBiasLeague.length === 1 && mySoloBiasLeague[0] === '') || (token === '' || !token)) {
                return (token ? <div className="setting">최애 설정이 필요합니다!</div> :
                    <div className="setting">로그인이 필요합니다!</div>
                )
            }
            else {
                return <League url={url} leagues={mySoloBiasLeague} isClicked={isSoloClicked}></League>
            }
        }
    }
    else if (isGroupClicked) {
        {
            if ((myGroupBiasLeague.length === 1 && myGroupBiasLeague[0] === '') || (token === '' || !token)) {
                return (token ? <div className="setting">최애 그룹 설정이 필요합니다!</div> :
                    <div className="setting">로그인이 필요합니다!</div>
                )
            }
            else {
                return <League url={url} leagues={myGroupBiasLeague} isClicked={isGroupClicked}></League>
            }
        }
    }
    else {
        return (
            <League url={url} leagues={leagues} isClicked={isSoloClicked || isGroupClicked}></League>
        )
    }
}

export default Meta;