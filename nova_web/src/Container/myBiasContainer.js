import { useEffect, useState } from "react";
import MySoloBias from "../component/subscribeBias/mySoloBias";
import MyGroupBias from "../component/subscribeBias/myGroupBias";

function MyBias({ url, token,showBox,blackBox }) {

    let [solo_bias, setSoloBias] = useState([]);
    let [group_bias, setGroupBias] = useState([]);

    let solo_bias_copy = [];
    let group_bias_copy = [];

    let [supportBias, setSupportBias] = useState();
    let supportBiasCopy = [];

    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }

    // let sample = localStorage.getItem('jwtToken');

    let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJhbmRvbVVzZXIxQG5hdmVyLmNvbSIsImlhdCI6MTcyNDE3MzUzMiwiZXhwIjoxNzI0MTc1MzMyfQ.FCJV4cO8V62-mBPIoeCtxT-dH_9qkbL8yHdKU9F33lY';

    let send_data = {
        "header": header,
        "body": {
            'token': token
        }
    }

    let my_bias_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    useEffect(() => {
        if (!token) {
            console.log('로그인 안됨')
        }
        else {
            fetch(url + 'my_bias',
                {
                    method: 'POST',
                    headers: {
                        "Content-Type": 'application/json',
                    },
                    body: JSON.stringify(send_data),
                })
            .then(response => response.json())
            .then(data => {
                solo_bias_copy = data.body.solo_bias;
                group_bias_copy = data.body.group_bias;

                setSoloBias(solo_bias_copy);
                setGroupBias(group_bias_copy);
                console.log('솔로 그룹 바이어스 부분');
            })
        }
    }, [token])

    return (
        <>
            <MySoloBias solo_bias={solo_bias} bias_url={my_bias_url} token={token} showBox={showBox} blackBox={blackBox}></MySoloBias>
            <MyGroupBias group_bias={group_bias} bias_url={my_bias_url} token={token} showBox={showBox} blackBox={blackBox}></MyGroupBias>
        </>
    )
}

export default MyBias;