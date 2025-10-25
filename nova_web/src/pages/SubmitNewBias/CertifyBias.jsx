import { useEffect, useState} from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import style from "./SubmitNewBias.module.css";
import title_star from "./title_star.svg";
import info from "./Info.svg";
import positive_icon from "./positive.svg";
import negative_icon from "./negative.svg";
import useMediaQuery from '@mui/material/useMediaQuery';
import DesktopLayout from '../../component/DesktopLayout/DeskTopLayout';
import mainApi from '../../services/apis/mainApi';
import HEADER from '../../constant/header';
import Header from "../../component/Header/Header";
import ReCAPTCHA from 'react-google-recaptcha';

const TEXT = {
  title: "스트리머 전용 계정 등록",
  subtitle: "스트리머라면 전용 계정으로 직접 관리해요!",
};

export default function CertifyBiasPage(){
    const isMobile = useMediaQuery('(max-width:1100px)');

    if(isMobile){
        return(
            <CertifyBiasComponent/>
        );
    }else{
        return(
            <DesktopLayout>
                <CertifyBiasComponent/>
            </DesktopLayout>
        );
    }

}


const CertifyBiasComponent= () => {
    const navigate = useNavigate();
    const location = useLocation();

    const [captcha, setCaptcha] = useState("");

    const handleCaptcha = (value) => {
        setCaptcha(value);
    };


    function handleFetch() {
        fetch("https://supernova.io.kr/home/is_valid", {
        credentials: "include", // 쿠키를 함께 포함한다는 것
        })
        .then((response) => {
            if (!response.ok) {
                if (response.status === 401) {
                    if (window.confirm("로그인이 필요합니다.")){
                        navigate("/novalogin", { state: { from: location.pathname } });
                    }else{
                        navigate("/");
                    }
                    return Promise.reject();
                }
            }
            return response
        })
        .then((data) => {
            if (data) {
            //console.log(data);
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
        });
    }

    useEffect(() => {
        handleFetch();
    }, []);

    const [value, setValue] = useState("");
    const onChangeValue = (e) => {
        const input = e.target.value.trimStart(); // 앞 공백 제거
        if (input.length <= 10) {
            setValue(input);
        }
    };

    return (
        <div className="container">
            <Header/>
            <div className={style["submit-page-frame"]}>
                {/* 제목 영역 */}
                <div className={style["default-container"]}>
                    <div className={style["title-wrapper"]}>
                        <div className={style["title-icon"]}>
                            <img src={title_star} />
                        </div>
                        <div className={style["title"]}>{TEXT.title}</div>
                    </div>
                    <div className={style["sub-title"]}>{TEXT.subtitle}</div>
                </div>

                <div className={style["default-container2"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title-icon"]}>
                        <img src={info} />
                        </div>
                        <div className={style["container-title"]}>STEP 1</div>
                    </div>
                    <div className={style["info-detail2"]}>
                        {
                            " SUPERNOVA 운영진과 직접 이메일로 컨택하세요! \n실제 스트리머라는 것을 증명하기만 하면 됩니다.  "
                        }
                    </div>
                </div>
                <div className={style["default-container2"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title-icon"]}>
                        <img src={info} />
                        </div>
                        <div className={style["container-title"]}>STEP 2</div>
                    </div>
                    <div className={style["info-detail2"]}>
                        {
                            "SUPERNOVA에 로그인 하고 이 페이지로 돌아오세요!"
                        }
                    </div>
                </div>
                <div className={style["default-container2"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title-icon"]}>
                        <img src={info} />
                        </div>
                        <div className={style["container-title"]}>STEP 3</div>
                    </div>
                    <div className={style["info-detail2"]}>
                        {
                            "운영진이 알려준 스트리머 전용 코드를 이곳에 넣으세요! \n반드시 운영진이 알려준 코드만 사용하셔야 합니다. "
                        }
                    </div>
                    <input
                        className={style["single-line-input-box"]}
                        placeholder={"12343"}
                        enterKeyHint="done"
                        value={value}
                        onChange={onChangeValue}
                    />
                </div>
                <div className={style["default-container2"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title-icon"]}>
                        <img src={info} />
                        </div>
                        <div className={style["container-title"]}>STEP 4</div>
                    </div>
                    <div className={style["info-detail2"]}>
                        {
                            "비정상적인 요청을 반복하는 계정은 운영 지침에 따라 제재될 수 있습니다."
                        }
                    </div>
                    <div style ={{
                    marginBottom: "10px"
                    }}>
                    <ReCAPTCHA
                        sitekey="6LePWrErAAAAAHE58_Rrc2Cxe9j01Ioxu8hZaysO"
                        onChange={handleCaptcha}
                    />
                    <p style={{ display:"flex", justifyContent:"center", marginBottom: "8px", color: "#ff7676ff" }}>
                        보안을 위해 캡차 인증을 완료해 주세요.
                    </p>
                    </div>
                    <div className={style["submit-button-wrapper"]}>
                        <div className={style["submit-button"]}
                            onClick={()=>{
                                if (captcha){
                                    alert("준비중입니다.")
                                }else{
                                    alert("보안을 위해 캡챠 인증을 완료해주세요.")
                                }
                            }
                            }
                        >
                            등록하기
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
