import { useEffect, useState } from "react";

function MyBiasRank() {
        if (isTouched === '내 최애') {
            let header = {
                "request-type": "default",
                "client-version": 'v1.0.1',
                "client-ip": '127.0.0.1',
                "uid": '1234-abcd-5678',
                "endpoint": "/core_system/",
            }
            let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzk5NDMzMCwiZXhwIjoxNzIzOTk2MTMwfQ.PWzlMUMKjMrgxc8Yl59-eIQPLP0QasunTnNl487ZWMA'
            let send_data = {
                "header": header,
                "body": {
                    'token': jwt
                }
            }
            return (
                <div className='행성 ' key={i}>
                <button onClick={() => {
                    fetch(url + "/my_bias_league",{
                    method: 'POST',
                    headers: {
                        "Content-Type": 'application/json',
                    },
                    body: JSON.stringify(send_data)
                    })
                    .then(response => response.json())
                    .then(data => {
                        rank_copy = [...data.body.rank]
                        setRank(rank_copy);
                        setClickedIndex(i);
                    })
                }} className={clickedIndex === i ? 'click-now' : 'non-click'} click>{leagues[i]}</button>
                </div>
            );
        }else{
            leagues.map(function (b, i) {
                return (
                    <div className='행성 ' key={i}>
                    <button onClick={() => {
                        fetch(url + `show_league?league_name=${[leagues[i]]}`)
                        .then(response => response.json())
                        .then(data => {
                            rank_copy = [...data.body.rank]
                            setRank(rank_copy);
                            setClickedIndex(i);
                        })
                    }} className={clickedIndex === i ? 'click-now' : 'non-click'} click>{leagues[i]}</button>
                    </div>
                );
            })
        }
    }

export default MyBiasRank;