import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import style from './../FeedPage/FeedPage.module.css';
import stylePlanet from './../PlanetPage/Planet.module.css';
import backword from "./../../img/back_icon.png";
import forward from "./../../img/Icon.png";
import back from "./../../img/backword.png";


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
    // const [isClickedBtn, setIsClickedBtn] = useState('card'); // 버튼 클릭 상태

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setImageFile(selectedFile);
        } else {
            setImageFile(null);
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();  // 기본 동작을 막음 (중요)

        const send_data = {
            header: header,
            body: {
                body: bodyText, // 입력된 글 본문 반영
                fid: "",
                fclass: currentFclass,
                choice: currentFclass === 'multiple' ? choice : [''], // 4지선다 선택지 반영
            },
        };

        const formData = new FormData();
        if (imageFile) {
            formData.append('image', imageFile);
        }
        formData.append('jsonData', JSON.stringify(send_data)); // JSON 데이터 추가

        fetch('https://nova-platform.kr/feed_explore/try_edit_feed', {
            method: 'POST',
            credentials: 'include',
            body: formData,
        })
            .then(response => {
                console.log(formData);
                response.json()
            })
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

    let title = ['줄 글', '사지선다', '이지선다', '외부 좌표'];
    let fclassName = ['card', 'multiple', 'balance', 'station'];
    let [currentTitle, setCurrentTitle] = useState(0);
    let [currentFclass, setCurrentFclass] = useState('card');
    // let [writeTitle, setWriteTitle] = useState();

    function handlePrev() {
        setCurrentTitle((prevIndex) => {
            return (prevIndex === 0 ? title.length - 1 : prevIndex - 1);
        })
        setCurrentFclass((prevIndex) => {
            return (prevIndex === 0 ? title.length - 1 : prevIndex - 1);
        })
    }
    function handleNext() {
        setCurrentTitle((prevIndex) => {
            return (prevIndex === title.length - 1 ? 0 : prevIndex + 1);
        });
        setCurrentFclass((prevIndex) => {
            return (prevIndex === title.length - 1 ? 0 : prevIndex + 1);
        });

    }

    return (
        <div className={style['test_container']}>
            <div className={`${stylePlanet['top_area']} ${style['top_bar_area']}`}>
                <img src={backword} alt="Arrow"
                    className={style.backword}
                    onClick={() => {
                        navigate(-1);
                    }}
                />
                <div className={style['write_select']}>
                    <div className={style['fclass_btn']}>
                        <img className={style['order_btn']} src={back} alt='prev'
                            onClick={handlePrev}></img>
                        <div>{title[currentTitle]}</div>

                        {/* <div onClick={() => setIsClickedBtn('card')}>줄 글</div> */}
                        {/* <button onClick={() => setIsClickedBtn('balance')}>둘중</button>
                        <button onClick={() => setIsClickedBtn('multiple')}>4지선다</button>
                        <button onClick={() => setIsClickedBtn('station')}>정거장</button> */}
                        <img className={style['order_btn']} src={forward} alt='next'
                            onClick={handleNext}></img>
                    </div>
                </div>
            </div>

            <div style={{ height: '50px' }}></div>
            <div className={style.test} >
                <div className={style['short_form_container']}>
                    <div className={style['short_box']}>
                        <div className={`${style['img_circle']} ${style['upload_area']}`}>
                            <input type='file' onChange={handleFileChange}></input>
                        </div>
                        <div style={{ height: '110px' }}></div>
                        <div className={`${style['short_feed']} ${style['write_feed']}`}>
                            <div style={{ height: '80px' }}></div>
                            <div className={`${style['write_container']} `}>
                                <form onSubmit={handleSubmit}>
                                    <div className={style['text_body']}>
                                        <textarea
                                            name='body'
                                            placeholder='내용을 입력해주세요'
                                            className={style['write_body']}
                                            value={bodyText}
                                            onChange={(e) => setBodyText(e.target.value)} // 본문 내용 상태 업데이트
                                        ></textarea>
                                    </div>

                                    <div className={style['contents_area']}>
                                        {/* 4지선다 */}
                                        {currentTitle === 1 && (
                                            <div className={style['one_of_four_area']}>
                                                <ol className={style['one_of_four_list']}>
                                                    {choice.map((ch, index) => (
                                                        <li key={index}>
                                                            {index + 1}. <input name='select' value={ch} onChange={(e) => handleChoiceChange(index, e.target.value)}></input>
                                                        </li>
                                                    ))}
                                                </ol>
                                            </div>
                                        )}
                                        {/* 둘 중 하나 */}
                                        {
                                            currentTitle === 2 && (
                                                <div>
                                                    <div className={`${style['button_container']}`}>
                                                        <input name='balance' maxLength={10} className={`${style['select_button']} ${style['balance_btn']}`}
                                                            onChange={(e) => handleChoiceChange(0, e.target.value)}></input>
                                                        <input name='balance' maxLength={10} className={`${style['select_button']} ${style['balance_btn']}`}
                                                            onChange={(e) => handleChoiceChange(1, e.target.value)}></input>
                                                    </div>
                                                </div>
                                            )
                                        }
                                        {/* 정거장 */}
                                        {
                                            currentTitle === 3 && (
                                                <div className={style['station_container']}>
                                                    <div className={style['station_box']}>
                                                        <input name='site_name' type='text' className={style['site_name']} placeholder='사이트 이름'
                                                            onChange={(e) => handleChoiceChange(0, e.target.value)}></input>
                                                        <input name='script' type='text' className={style['site_script']} placeholder='설명'
                                                            onChange={(e) => handleChoiceChange(1, e.target.value)}></input>
                                                        <input name='url' type='url' className={style['site_url']} placeholder='url'
                                                            onChange={(e) => handleChoiceChange(2, e.target.value)}></input>
                                                    </div>
                                                </div>
                                            )
                                        }
                                        {
                                            currentTitle === 0 && <div></div>
                                        }
                                    </div>

                                    <div className={style['func_part']}>
                                        <div className={style['btn_func_area']}>
                                            <div className={style['btn_func']}>
                                                <label>
                                                    <input name='comment' type='checkbox'></input>댓글 허용
                                                </label>
                                                <label>
                                                    <input name='share' type='checkbox'></input>공유 허용
                                                </label>
                                            </div>
                                            <button type='submit'>업로드</button>
                                        </div>
                                        <div className={style['warning_text']}>타인에게 불편을 줄 수 있는 내용의 게시글은 경고 없이 삭제될 수 있습니다.</div>

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