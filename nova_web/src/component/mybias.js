import { useEffect, useState } from "react";
import more from '../img/more.png';

function MyBias() {

    let [bias, setBias] = useState([]);
    let bias_copy = [];

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

    let select_bias_send_data = {
        "header": header,
        "body": {
            'token': jwt,
            'bid': 1001,
        }
    }

    let url = 'http://175.106.99.34/home/';
    let bias_url = url + 'my_bias';
    let solo_bias_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    useEffect(() => {
        fetch(bias_url, {
            method: 'POST',
            headers: {
                "Content-Type": 'application/json',
            },
            body: JSON.stringify(send_data),
        })
            .then(response => response.json())
            .then(data => {
                bias_copy = data.body.solo_bias;
                setBias(bias_copy);
            })
    }, [bias_url])


    return (
        <div className='left-box'>
            <img src={solo_bias_url + `${bias.bid}.PNG`}></img>
            <div className='support'>지지하기</div>
            <div className='box'>
                <div className='my-bias-solo'>나의 최애</div>
                <div className='bias-name'>{bias.bname}</div>
            </div>
            <div className='more'>
                <img src={more}></img>
            </div>
        </div>
    )
}

export default MyBias;