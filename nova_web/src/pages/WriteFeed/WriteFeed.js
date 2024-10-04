// import Feed, { InputFeed, InfoArea, Text, Comments } from '../../component/feed';

// import style from './../FeedPage/FeedPage.module.css';
// import stylePlanet from './../PlanetPage/Planet.module.css';

// import React, { useState, useEffect, useRef } from 'react';
// // import style from './../pages/FeedPage/FeedPage.module.css';
// import { useLocation, useNavigate } from 'react-router-dom';

// const WriteFeed = () => {

//     let header = {
//         "request-type": "default",
//         "client-version": "v1.0.1",
//         "client-ip": "127.0.0.1",
//         "uid": "1234-abcd-5678",
//         "endpoint": "/user_system/",
//     };

//     const send_data = {
//         header: header,
//         body: {
//             body: "1",
//             fid: "1",
//             fclass: "balance",
//             choice: [],
//         },
//     };

//     let [imageFile, setImageFile] = useState(null);

//     const handleFileChange = (event) => {
//         setImageFile(event.target.files[0]);
//     };

//     // const formData = new FormData();
//     // formData.append('image', imageFile);


//     let navigate = useNavigate();

//     let [isClickedBtn, setIsClickedBtn] = useState('card');

//     function handleBtn(fclass) {
//         setIsClickedBtn(fclass);
//     };

//     function handleSubmit() {
//         const formData = new FormData();
//         formData.append('image', imageFile);
//         formData.append('jsonData', JSON.stringify(send_data));

//         fetch('https://nova-platform.kr/feed_explore/try_edit_feed', {
//             method: 'POST',
//             credentials: 'include',
//             body: formData,
//         })
//             .then(response => response.json())
//             .then(data => {
//                 console.log(data)
//             })
//     }


//     // function handleFetchSend() {
//     //     fetch('https://nova-platform.kr/feed_explore/try_edit_feed', {
//     //         method: 'POST',
//     //         credentials: 'include',
//     //         headers: {
//     //             "Content-Type": 'application/json',
//     //         },
//     //         body: JSON.stringify(send_data),
//     //     })
//     // };


//     return (
//         <div className={style['test_container']}>
//             <div className={`${stylePlanet['top_area']} ${style['top_bar_area']}`}>
//                 <div onClick={() => { navigate(-1) }}>뒤로</div>
//                 <div className={style['write_select']}>
//                     <button onClick={() => handleBtn('card')}>카드</button>
//                     <button onClick={() => handleBtn('balance')}>둘중</button>
//                     <button onClick={() => handleBtn('multiple')}>4지선다</button>
//                     <button onClick={() => handleBtn('station')}>정거장</button>
//                 </div>
//             </div>

//             <div style={{ height: '50px' }}></div>
//             <div className={style.test} >
//                 <div className={style['short_form_container']}>
//                     <div className={style['short_box']}>
//                         <form onSubmit={handleSubmit}>
//                             <div className={style['img_circle']}>
//                                 <input type='file' onChange={(e) => handleFileChange}></input>
//                             </div>
//                             <div style={{ height: '110px' }}></div>
//                             <div className={`${style['short_feed']} ${style['write_feed']}`}>
//                                 <div style={{ height: '80px' }}></div>
//                                 <div className={`${style['write_container']} `}>

//                                     <div className={style['text_body']}>
//                                         <textarea placeholder='내용을 입력해주세요' className={style['write_body']}></textarea>
//                                     </div>

//                                     <div className={style['contents_area']}>
//                                         {/* 넷중하나 */}
//                                         {
//                                             isClickedBtn === 'multiple' && (
//                                                 <div className={style['one_of_four_area']}>
//                                                     <ol className={style['one_of_four_list']}>
//                                                         <li>
//                                                             1. <input></input>
//                                                         </li>
//                                                         <li>
//                                                             2. <input></input>
//                                                         </li>
//                                                         <li>
//                                                             3. <input></input>
//                                                         </li>
//                                                         <li>
//                                                             4. <input></input>
//                                                         </li>
//                                                     </ol>
//                                                 </div>
//                                             )
//                                         }

//                                         {/* 둘 중 하나 */}
//                                         {
//                                             isClickedBtn === 'balance' && (
//                                                 <div>
//                                                     <div className={`${style['button_container']}`}>
//                                                         <input maxLength={10} className={`${style['select_button']} ${style['balance_btn']}`}></input>
//                                                         <input className={`${style['select_button']} ${style['balance_btn']}`}></input>
//                                                     </div>
//                                                 </div>
//                                             )
//                                         }

//                                         {/* 정거장 */}
//                                         {
//                                             isClickedBtn === 'station' && (
//                                                 <div className={style['station_container']}>
//                                                     <div className={style['station_box']}>
//                                                         <input type='text' className={style['site_name']} placeholder='사이트 이름'></input>
//                                                         <input type='text' className={style['site_script']} placeholder='설명'></input>
//                                                         <input type='url' className={style['site_url']} placeholder='url'></input>
//                                                     </div>
//                                                 </div>
//                                             )
//                                         }
//                                         {
//                                             isClickedBtn === 'card' && <div></div>
//                                         }

//                                     </div>

//                                     <div className={style['func_part']}>
//                                         <div className={style['btn_func_area']}>
//                                             <div className={style['btn_func']}>
//                                                 <label>
//                                                     <input type='checkbox'></input>댓글 허용
//                                                 </label>
//                                                 <label>
//                                                     <input type='checkbox'></input>공유 허용
//                                                 </label>
//                                             </div>
//                                             <button type='submit' >업로드</button>
//                                         </div>

//                                         <div className={style['warning_text']}>타인에게 불편을 줄 수 있는 내용의 게시글은 경고 없이 삭제될 수 있습니다.</div>
//                                     </div>

//                                 </div>
//                             </div>
//                         </form>

//                     </div>
//                 </div>
//             </div>

//         </div>
//     );
// };

// export default WriteFeed;


import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import style from './../FeedPage/FeedPage.module.css';
import stylePlanet from './../PlanetPage/Planet.module.css';

const WriteFeed = () => {
    const navigate = useNavigate();

    let header = {
        "request-type": "default",
        "client-version": "v1.0.1",
        "client-ip": "127.0.0.1",
        "uid": "1234-abcd-5678",
        "endpoint": "/user_system/",
    };

    const [imageFile, setImageFile] = useState(null);
    const [bodyText, setBodyText] = useState(''); // 글 입력 내용 상태로 저장
    const [choice, setChoice] = useState(['', '', '', '']); // 선택지 4개 상태로 저장
    const [isClickedBtn, setIsClickedBtn] = useState('card'); // 버튼 클릭 상태

    const handleFileChange = (event) => {
        setImageFile(event.target.files[0]);
    };

    const handleSubmit = (event) => {
        event.preventDefault();  // 기본 동작을 막음 (중요)

        const send_data = {
            header: header,
            body: {
                body: bodyText, // 입력된 글 본문 반영
                fid: "",
                fclass: isClickedBtn,
                choice: isClickedBtn === 'multiple' ? choice : [], // 4지선다 선택지 반영
            },
        };

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('jsonData', JSON.stringify(send_data)); // JSON 데이터 추가

        fetch('https://nova-platform.kr/feed_explore/try_edit_feed', {
            method: 'POST',
            credentials: 'include',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };

    const handleChoiceChange = (index, value) => {
        const newChoices = [...choice];
        newChoices[index] = value;
        setChoice(newChoices); // 4지선다 선택지 업데이트
    };

    return (
        <div className={style['test_container']}>
            <div className={`${stylePlanet['top_area']} ${style['top_bar_area']}`}>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div className={style['write_select']}>
                    <button onClick={() => setIsClickedBtn('card')}>카드</button>
                    <button onClick={() => setIsClickedBtn('balance')}>둘중</button>
                    <button onClick={() => setIsClickedBtn('multiple')}>4지선다</button>
                    <button onClick={() => setIsClickedBtn('station')}>정거장</button>
                </div>
            </div>

            <div style={{ height: '50px' }}></div>
            <div className={style.test} >
                <div className={style['short_form_container']}>
                    <div className={style['short_box']}>
                        <div className={style['img_circle']}>
                            <input type='file' onChange={handleFileChange}></input>
                        </div>
                        <div style={{ height: '110px' }}></div>
                        <div className={`${style['short_feed']} ${style['write_feed']}`}>
                            <div style={{ height: '80px' }}></div>
                            <div className={`${style['write_container']} `}>
                                <form onSubmit={handleSubmit}>
                                    <div className={style['text_body']}>
                                        <textarea
                                            placeholder='내용을 입력해주세요'
                                            className={style['write_body']}
                                            value={bodyText}
                                            onChange={(e) => setBodyText(e.target.value)} // 본문 내용 상태 업데이트
                                        ></textarea>
                                    </div>

                                    <div className={style['contents_area']}>
                                        {/* 4지선다 */}
                                        {isClickedBtn === 'multiple' && (
                                            <div className={style['one_of_four_area']}>
                                                <ol className={style['one_of_four_list']}>
                                                    {choice.map((ch, index) => (
                                                        <li key={index}>
                                                            {index + 1}. <input value={ch} onChange={(e) => handleChoiceChange(index, e.target.value)}></input>
                                                        </li>
                                                    ))}
                                                </ol>
                                            </div>
                                        )}
                                    </div>

                                    <div className={style['func_part']}>
                                        <div className={style['btn_func_area']}>
                                            <button type='submit'>업로드</button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default WriteFeed;