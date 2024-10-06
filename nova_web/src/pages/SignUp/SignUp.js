import { useEffect, useState } from 'react';
import style from './SignUp.module.css';
import { useNavigate } from 'react-router-dom';

export default function SignUp() {

    let [inputEmail, setInputEmail] = useState('');
    let [authen, setAuthen] = useState(false);
    let [code, setCode] = useState('')
    let [pwd, setPwd] = useState('');
    let [checkPwd, setCheckPwd] = useState('');
    let [age, setAge] = useState('');
    let [gender, setGender] = useState('');

    let [result, setResult] = useState(false);
    let navigate = useNavigate();

    let header = {
        "request-type": "default",
        "client-version": "v1.0.1",
        "client-ip": "127.0.0.1",
        "uid": "1234-abcd-5678",
        "endpoint": "/user_system/",
    };

    let send_data = {
        header: header,
        body: {
            email: inputEmail
        }
    };

    let signUp_data = {
        header: header,
        body: {
            email: inputEmail,
            password: pwd,
            verification_code: code,
            age: age,
            gender: gender,
        }
    };

    function handleInputEmail(e) {
        setInputEmail(e.target.value);
    };
    function handlePassWord(e) {
        setPwd(e.target.value);
    };
    function handleCheckPassWord(e) {
        setCheckPwd(e.target.value);
    };
    function handleAge(e) {
        setAge(e.target.value)
    };
    function handleGender(e) {
        setGender(e.target.value)
    };
    function handleCode(e) {
        setCode(e.target.value)
    };

    useEffect(() => {
        return (
            setInputEmail('')
        )
    }, []);

    function fetchAuthenEmail() {

        fetch(`https://nova-platform.kr/user_home/try_send_email`, {
            headers: {
                "Content-Type": 'application/json',
            },
            method: 'POST',
            body: JSON.stringify(send_data)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setAuthen(data.body.result);
            })
        alert('인증코드가 전송되었습니다');

    };

    function fetchSignUp() {
        fetch(`https://nova-platform.kr/user_home/try_sign_in`, {
            headers: {
                "Content-Type": 'application/json',
            },
            method: 'POST',
            body: JSON.stringify(signUp_data)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.body.result) {
                    alert('회원가입이 완료되었습니다.');
                    navigate('/novalogin');
                }
                // setResult(data.body.result);
            })
    };

    function handleSubmit(e) {
        e.preventDefault();

        if (pwd !== checkPwd) {
            alert('비밀번호가 같지 않습니다.');
            return
        }
        fetchSignUp()
    };

    // function handleStart() {
    //     if (result) {
    //         alert('회원가입이 완료되었습니다.');
    //         navigate('/novalogin');
    //     }
    // };



    return (
        <div className={style.container}>
            <div className={style.title}>회원가입</div>
            <div>
                <form onSubmit={(e) => handleSubmit(e)}>
                    <div className={style.box}>
                        <div className={style.test}>
                            이메일
                            <br />
                            <label>
                                <input type='email' name='email' value={inputEmail}
                                    onChange={(e) => handleInputEmail(e)}
                                    required ></input>
                                <button className={style.authen} disabled={!inputEmail}
                                    style={{
                                        background: inputEmail ? '#98A0FF' : '',
                                        color: inputEmail ? 'white' : ''
                                    }}
                                    onClick={() => {
                                        fetchAuthenEmail()
                                    }}>인증</button>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            인증번호
                            <br />
                            <label>
                                <input name='password' required onChange={(e) => { handleCode(e) }}></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            비밀번호
                            <br />
                            <label>
                                <input type='password' name='password' required
                                    onChange={(e) => handlePassWord(e)}></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            비밀번호 확인
                            <br />
                            <label>
                                <input type='password' name='check_pwd' required
                                    onChange={(e) => handleCheckPassWord(e)}></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            나이
                            <br />
                            <label>
                                <input type='number' name='age' required
                                    onChange={(e) => handleAge(e)}></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            성별
                            <br />
                            <input type='radio' name='gender' id='gender1' required
                                onChange={(e) => handleGender(e)}></input>
                            <label htmlFor='gender1'>남성</label>

                            <input type='radio' name='gender' id='gender2' required
                                onChange={(e) => handleGender(e)} ></input>
                            <label htmlFor='gender2'>여성</label>

                            <input type='radio' name='gender' id='gender3' required
                                onChange={(e) => handleGender(e)} ></input>
                            <label htmlFor='gender3'>기타</label>

                            <input type='radio' name='gender' id='gender4' required
                                onChange={(e) => handleGender(e)} ></input>
                            <label htmlFor='gender4'>비공개</label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            약관 동의
                            <br />
                            <div className={style['agree_box']}>
                                <label>
                                    <input type='checkbox' name='agree1' required></input>
                                    (필수) 이용약관 동의
                                </label>
                                <br />
                                <label>
                                    <input type='checkbox' name='agree2' required></input>
                                    (필수) 개인정보처리 동의
                                </label>
                            </div>
                        </div>
                    </div>

                    <div className={style['submit_area']}>
                        <button type='submit' className={style['submit_btn']}>노바 시작하기</button>
                    </div>
                </form>
            </div >
        </div >
    )
}