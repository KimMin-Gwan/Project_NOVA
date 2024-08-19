import { useEffect, useState } from "react";
import MySoloBias from "../component/subscribeBias/mySoloBias";
import MyGroupBias from "../component/subscribeBias/myGroupBias";

function MyBias() {

    let [solo_bias, setSoloBias] = useState([]);
    let [group_bias, setGroupBias] = useState([]);

    let solo_bias_copy = [];
    let group_bias_copy = [];


    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }

    let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyNDA0MDA1MCwiZXhwIjoxNzI0MDQxODUwfQ.WxZ9UAhZlD0hkNcyvc4rPN_IIraVr2oZSXvTuTteaQU'

    let send_data = {
        "header": header,
        "body": {
            'token': jwt
        }
    }

    let select_bias_send_data = {
        "header": header,
        "body": {
            'token': jwt,
            'bid': 1001,
        }
    }

    let url = 'http://175.106.99.34/home/';
    let my_bias_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    useEffect(() => {
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
            })
    }, [])

    return (
        <div>
            <MySoloBias solo_bias={solo_bias} bias_url={my_bias_url}></MySoloBias>
            <MyGroupBias group_bias={group_bias} bias_url={my_bias_url}></MyGroupBias>
        </div>
    )
}

export default MyBias;