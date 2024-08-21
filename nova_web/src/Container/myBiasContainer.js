import { useEffect, useState } from "react";
import MySoloBias from "../component/subscribeBias/mySoloBias";
import MyGroupBias from "../component/subscribeBias/myGroupBias";

function MyBias({url}) {

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

    let sample = localStorage.getItem('jwtToken');
    
    let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJhbmRvbVVzZXIxQG5hdmVyLmNvbSIsImlhdCI6MTcyNDE3MzUzMiwiZXhwIjoxNzI0MTc1MzMyfQ.FCJV4cO8V62-mBPIoeCtxT-dH_9qkbL8yHdKU9F33lY';
    
    let send_data = {
        "header": header,
        "body": {
            'token': sample
        }
    }
    
    let select_bias_send_data = {
        "header": header,
        "body": {
            'token': sample,
            'bid': 1001,
        }
    }

    // useEffect(()=>{
    //     fetch(url+'try_select_my_bias',
    //         {
    //             method: 'POST',
    //             headers: {
    //                 "Content-Type": 'application/json',
    //             },
    //             body: JSON.stringify(select_bias_send_data),
    //         }
    //     )
    //     .then(response=>response.json())
    //     .then(data=>{
    //         supportBiasCopy = data.body;
    //         console.log(supportBiasCopy);
    //         console.log('지지하기 바이어스');
            
    //     })
    // },[url])

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
                console.log(data)
            })
    }, [])

    return (
        <>
            <MySoloBias solo_bias={solo_bias} bias_url={my_bias_url}></MySoloBias>
            <MyGroupBias group_bias={group_bias} bias_url={my_bias_url}></MyGroupBias>
        </>
    )
}

export default MyBias;