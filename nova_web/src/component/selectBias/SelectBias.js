import style from './SelectBias.module.css';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';



function SelectBias({ selectWindow, setSelectWindow }) {

    let navigate = useNavigate();
    let url = 'https://nova-platform.kr/home/';
    // let url = 'http://127.0.0.1:5000/home/';

    let header = {
        "request-type": "default",
        "client-version": 'v1.0.1',
        "client-ip": '127.0.0.1',
        "uid": '1234-abcd-5678',
        "endpoint": "/core_system/",
    }

    let sample = localStorage.getItem('jwtToken');

    // let select_bias_send_data = {
    //     "header": header,
    //     "body": {
    //         'token': sample,
    //         'bid': 1001,
    //     }
    // }

    let [searchName, setSearchName] = useState('');
    let [results, setResults] = useState([]);
    let [loading, setLoading] = useState(false);

    // let [trySelect, setTrySelect] = useState(null);

    let nameCopy = [];

    function changeName(event) {
        setSearchName(event.target.value);
    };
    useEffect(() => {
        fetch(url + `search_bias?bias_name=${searchName}`, {
            credentials: 'include',
        })
            .then(result => result.json())
            .then(data => {
                nameCopy = JSON.stringify(data.body.biases);
                nameCopy = data.body.biases;
                setResults(nameCopy);
                // console.log(results);
            })

        // return setSearchName('');
    }, [searchName])


    if (!results) {
        return <p>eror</p>
    }


    return (
        <div className={style.background}>
            <div className={style.container}>
                <div className={style.header}>
                    <button onClick={() => {
                        setSelectWindow(false)
                    }}>뒤로</button>
                    <h1>지지할 최애 선택하기 (개인)</h1>
                    <p>(지지 대상은 변경할 수 없습니다)</p>
                </div>
                <div className={style['search-box']}>
                    <input type={style.text} value={searchName} onChange={changeName} placeholder="최애의 이름을 검색해보세요." />
                    <button >검색</button>
                </div>
                {
                    loading && <p>로딩 중....</p>
                }

                <div className={style["favorites-list"]}>
                    {
                        results.map(function (a, i) {
                            return (
                                <div key={i} className={style["favorite-item"]}>
                                    <div className={style["favorite-info"]}>
                                        <h3>{a.bname}</h3>
                                        <p>#온라인콘텐츠창작자 #QWER</p>
                                    </div>
                                    <button className={style["heart-button"]} onClick={() => {
                                        fetch(url + `try_select_my_bias`, {
                                            method: 'POST',
                                            headers: {
                                                "Content-Type": 'application/json',
                                            },
                                            body: JSON.stringify({
                                                "header": header,
                                                "body": {
                                                    'bid': a.bid,
                                                }
                                            }),
                                            credentials: 'include',
                                        })
                                            .then(result => result.json())
                                            .then(data => {
                                                // JSON.stringify(data.body);
                                                console.log(data);
                                            })
                                    }}>&#9825;</button>
                                </div>
                            )
                        })
                    }
                </div>
            </div>
        </div>
    )
}

export default SelectBias;