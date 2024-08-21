import { useState, useEffect } from "react";
import League from "../component/league";

function Meta({ url, isClicked, type }) {

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
    let [myBiasLeague, setMyBiasLeague] = useState();

    let send_data = {
        "header": header,
        "body": {
            'token': sample,
            'type': type,
        }
    }

    useEffect(()=>{
        fetch(url+'my_bias_league',{
            method: 'post',
            headers: {
                "Content-Type": 'application/json',
            },
            body: JSON.stringify(send_data),
        })
        .then(response=>response.json())
        .then(data=>{
            my_bias_league_copy = data.body;
            console.log(my_bias_league_copy)
            setMyBiasLeague(my_bias_league_copy);
            console.log(myBiasLeague)
        })

    },[url])


    useEffect(() => {
        fetch(url + `league_data?league_type=${type}`)
            .then(response => response.json())
            .then(data => {
                league_copy = data.body.leagues.map(leagues => leagues.lname);
                setLeagues(league_copy);
            })
    }, [url])

    return (
        <League url={url} leagues={leagues} isClicked={isClicked} biasLeague={myBiasLeague}></League>
    )
}

export default Meta;