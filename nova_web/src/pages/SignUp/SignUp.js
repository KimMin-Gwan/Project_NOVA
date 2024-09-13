import style from './SignUp.module.css';

export default function SignUp() {
    return (
        <div className={style.container}>
            <div className={style.title}>회원가입</div>
            <div>
                <form action='' >
                    <div className={style.box}>
                        <div className={style.test}>
                            이메일
                            <br />
                            <label>
                                <input type='email' name='email' required></input>
                                <button className={style.authen}>인증</button>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            인증번호
                            <br />
                            <label>
                                <input  name='password' required></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            비밀번호
                            <br />
                            <label>
                                <input type='password' name='password' required></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            비밀번호 확인
                            <br />
                            <label>
                                <input type='password' name='check_pwd' required></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            나이
                            <br />
                            <label>
                                <input type='number' name='age' required></input>
                            </label>
                        </div>
                    </div>

                    <div className={style.box}>
                        <div className={style.test}>
                            성별
                            <br />
                            <input type='radio' name='gender1' id='gender1' required></input>
                            <label htmlFor='gender1'>남성</label>

                            <input type='radio' name='gender1' id='gender2' required></input>
                            <label htmlFor='gender2'>여성</label>

                            <input type='radio' name='gender1' id='gender3' required></input>
                            <label htmlFor='gender3'>기타</label>

                            <input type='radio' name='gender1' id='gender4' required></input>
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
                                    <br/>
                                    <input type='checkbox' name='agree2' required></input>
                                    (필수) 개인정보처리 동의
                                </label>
                            </div>
                        </div>
                    </div>
                    

                    <button type='submit'>노바 시작하기</button>
                </form>
            </div >
        </div >
    )
}