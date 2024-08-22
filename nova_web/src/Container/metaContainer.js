import { useState, useEffect } from "react";
import League from "../component/league";

function Meta({ url, isClicked,isSoloClicked, isGroupClicked, type }) {

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

    let my_bias_league_copy = [];
    let [mySoloBiasLeague, setMySoloBiasLeague] = useState([]);
    let [myGroupBiasLeague, setMyGroupBiasLeague] = useState([]);

    // let send_data = {
    //     "header": header,
    //     "body": {
    //         'token': sample,
    //         'type': type,
    //     }
    // }

    // useEffect(()=>{
    //     fetch(url+'my_bias_league',{
    //         method: 'post',
    //         headers: {
    //             "Content-Type": 'application/json',
    //         },
    //         body: JSON.stringify(send_data),
    //     })
    //     .then(response=>response.json())
    //     .then(data=>{
    //         my_bias_league_copy = data.body;

    //         setMyBiasLeague(my_bias_league_copy);
    //         console.log(myBiasLeague)
    //     })

    // },[url])
    useEffect(() => {
        const fetchSoloData = async () => {
            // let solo_send_data = {
            //     "header": header,
            //     "body": {
            //         'token': sample,
            //         'type': 'solo',
            //     }
            // }
            try {
                const response = await fetch(url + 'my_bias_league',
                    {
                        method: 'post',
                        headers: {
                            "Content-Type": 'application/json',
                        },
                        body: JSON.stringify({
                            "header": header,
                            "body": {
                                'token': sample,
                                'type': 'solo',
                            }
                        }),
                    }
                );
                const data = await response.json();
                console.log('솔로 데잍: ', data);

                setMySoloBiasLeague(data.body.league_data.lname);
            }
            catch (error) {
                console.error('Error fetching data: ', error);
            }
        };

        fetchSoloData();

    }, [url]);

    useEffect(()=>{
        const fetchGroupData = async () => {
            // let group_send_data = {
            //     "header": header,
            //     "body": {
            //         'token': sample,
            //         'type': 'group',
            //     }
            // }
            try {
                const response = await fetch(url + 'my_bias_league',
                    {
                        method: 'post',
                        headers: {
                            "Content-Type": 'application/json',
                        },
                        body: JSON.stringify({
                            "header": header,
                            "body": {
                                'token': sample,
                                'type': 'group',
                            }
                        }),
                    }
                );
                const data = await response.json();
                console.log('그룹 데이터: ', data);

                setMyGroupBiasLeague(data.body.league_data.lname);

            }
            catch (error) {
                console.error('Error fetching data: ', error);
            }
        };

        fetchGroupData();
    }, [url]);

    useEffect(() => {
        console.log(mySoloBiasLeague);
        console.log(myGroupBiasLeague);
        console.log('solo: ' + isSoloClicked + type);
        console.log('group: ', isGroupClicked + type);
    }, [mySoloBiasLeague, myGroupBiasLeague, isSoloClicked, isGroupClicked]);

    useEffect(() => {
        fetch(url + `league_data?league_type=${type}`)
            .then(response => response.json())
            .then(data => {
                league_copy = data.body.leagues.map(leagues => leagues.lname);
                setLeagues(league_copy);
            })
    }, [url])

    return (
        <League url={url} leagues={leagues} isClicked={isClicked}></League>
    )
}

export default Meta;