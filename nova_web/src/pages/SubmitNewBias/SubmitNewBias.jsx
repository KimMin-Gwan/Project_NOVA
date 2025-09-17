import { useEffect, useState} from 'react';
import { useNavigate } from "react-router-dom";
import style from "./SubmitNewBias.module.css";
import title_star from "./title_star.svg";
import info from "./Info.svg";
import positive_icon from "./positive.svg";
import negative_icon from "./negative.svg";
import useMediaQuery from '@mui/material/useMediaQuery';
import DesktopLayout from '../../component/DesktopLayout/DeskTopLayout';
import mainApi from '../../services/apis/mainApi';
import HEADER from '../../constant/header';

const TEXT = {
  title: "최애 주제 등록",
  subtitle: "슈퍼노바 앱에 새로운 스트리머를 등록하세요!",
  noticeTitle: "유의사항",
  noticeDesc:
    "아래에 유의 사항을 반드시 읽고 스트리머 정보를 제공해주세요!\n만약 약관에 위반되는 사항이 있을 경우 제출이 반려됩니다.",
  formTitle: "정보 작성",
  conditionTitle: "필수 조건",
  checkboxLabel: "위 필수조건을 확인 했습니다.",
  submitButton: "제출하기",
};

const formFields = [
  {
    label: "이름*",
    placeholder: "사용하는 닉네임을 적어주세요",
    multiline: false,
  },
  {
    label: "방송 플랫폼*",
    placeholder: "치지직 또는 SOOP으로 적어주세요",
    multiline: false,
  },
  {
    label: "관련 정보*",
    placeholder: "스트리머에 대한 추가 정보를 적어주세요",
    multiline: true,
  }
];

const mainConditions = [
  { type: "positive", text: "살아있는 사람만 등록 가능합니다." },
  {
    type: "positive",
    text: "치지직 또는 SOOP에서 스트리밍을 하는 인물이어야 합니다.",
  },
  { type: "negative", text: "가상의 인물은 등록할 수 없습니다." },
  { type: "negative", text: "정치와 관련 있는 인물은 등록할 수 없습니다." },
  { type: "negative", text: "논란이 있을 수 있는 인물은 등록할 수 없습니다." },
  { type: "negative", text: "일반인은 등록할 수 없습니다." },
];

const subConditions = [
  "제출을 하면 임시로 등록되며, 당사자가 인증을 수행하여 정식으로 등록됩니다.",
  "당사자의 거부가 있을 경우 언제든 사라질 수 있습니다.",
  "필수 조건에 부합하지 않은 임시 등록된 인물은 언제든 사라질 수 있습니다.",
];

export default function SubmitNewBiasPage(){
    const isMobile = useMediaQuery('(max-width:1100px)');

    if(isMobile){
        return(
            <SubmitNewBias/>
        );
    }else{
        return(
            <DesktopLayout>
                <SubmitNewBias/>
            </DesktopLayout>
        );
    }

}


function SubmitNewBias() {
    const navigate = useNavigate();

    function handleFetch() {
        fetch("https://supernova.io.kr/home/is_valid", {
        credentials: "include", // 쿠키를 함께 포함한다는 것
        })
        .then((response) => {
            if (!response.ok) {
                if (response.status === 401) {
                    alert("로그인이 필요한 서비스입니다.");
                    navigate("/novalogin");
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

    const [isChecked, setIsChecked] = useState(false);


    const [form, setForm] = useState({
        name: '',
        platform: '',
        info: '',
        email: '',
    });

    const [errors, setErrors] = useState({
        name: '',
        platform: '',
        info: '',
        email: '',
        checkbox: '',
    });


    const handleChange = (key) => (e) => {
        const value = e.target.value;
        setForm(prev => ({ ...prev, [key]: value }));
        setErrors(prev => ({ ...prev, [key]: '' }));
    };

    const handleCheckboxChange = (e) => {
        setIsChecked(e.target.checked);
        setErrors(prev => ({ ...prev, checkbox: '' }));
    };

    const handleSubmit = () => {
        const { name, platform, info} = form;
        const newErrors = {
            name: '',
            platform: '',
            info: '',
            checkbox: '',
        };

        if (!name.trim()) newErrors.name = '이름을 입력해주세요.';
        if (!platform.trim()) newErrors.platform = '플랫폼을 입력해주세요.';
        if (!info.trim()) newErrors.info = '관련 정보를 입력해주세요.';
        if (!isChecked) newErrors.checkbox = '필수조건을 확인해주세요.';

        setErrors(newErrors);

        // 모든 에러가 비어있을 때만 제출
        const hasError = Object.values(newErrors).some(msg => msg);
        if (!hasError) {
            console.log('제출 완료', form);
            fetchNewBias()
        }
        navigate('/');
    };

    const fetchNewBias = async () => {
        await mainApi.post("nova_sub_system/try_add_new_bias", {
                header: HEADER,
                body: form
            }
        ).then((res) => {
        });
    }


    const renderCondition = (condition, idx) => (
        <div key={idx} className={style["condition-wrapper"]}>
        <div
            className={
            condition.type === "positive"
                ? style["condition-positive-icon"]
                : style["condition-negative-icon"]
            }
        >
            <img src={condition.type === "positive" ? positive_icon : negative_icon} />
        </div>
        <div className={style["condition-detail"]}>{condition.text}</div>
        </div>
    );

    return (
        <div className="container">
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

                {/* 유의사항 */}
                <div className={style["default-container"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title-icon"]}>
                        <img src={info} />
                        </div>
                        <div className={style["container-title"]}>{TEXT.noticeTitle}</div>
                    </div>
                    <div className={style["info-detail"]}>
                        {TEXT.noticeDesc.split("\n").map((line, i) => (
                        <div key={i}>{line}</div>
                        ))}
                    </div>
                </div>

                {/* 입력 폼 */}
                <div className={style["default-container"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title"]}>{TEXT.formTitle}</div>
                    </div>
                    {formFields.map((field, index) => {
                        const key = ["name", "platform", "info", "email"][index];
                        return (
                            <div className={style["input-section"]} key={index}>
                            <div className={style["input-section-title"]}>{field.label}</div>
                            {field.multiline ? (
                                <textarea
                                className={style["multi-line-input-box"]}
                                placeholder={field.placeholder}
                                value={form[key]}
                                onChange={handleChange(key)}
                                />
                            ) : (
                                <input
                                className={style["single-line-input-box"]}
                                placeholder={field.placeholder}
                                value={form[key]}
                                onChange={handleChange(key)}
                                />
                            )}
                            {errors[key] && (
                                <div className={style["error-message"]}>{errors[key]}</div>
                            )}
                            </div>
                        );
                    })}
                    
                </div>

                {/* 조건 */}
                <div className={style["default-container"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title"]}>{TEXT.conditionTitle}</div>
                    </div>

                    {mainConditions.map(renderCondition)}

                    <div className={style["separater-line"]}></div>

                    <div className={style["sub-conditions-wrapper"]}>
                        {subConditions.map((text, idx) => (
                        <div className={style["sub-condition-wrapper"]} key={idx}>
                            <div className={style["sub-condition-detail"]}>{text}</div>
                        </div>
                        ))}
                    </div>
                </div>

                {/* 제출 */}
                <div className={style["default-container"]}>
                    <div className={style["container-title-wrapper"]}>
                        <div className={style["container-title"]}>제출</div>
                    </div>

                    <label className={style["checkbox-label"]}>
                        <input
                            type="checkbox"
                            className={style["checkbox-input"]}
                            checked={isChecked}
                            onChange={handleCheckboxChange}
                        />
                        <span className={style["checkbox-placeholder"]}>
                            {TEXT.checkboxLabel}
                        </span>
                    </label>
                    {errors.checkbox && (
                        <div className={style["error-message"]}>{errors.checkbox}</div>
                    )}

                    <div className={style["submit-button-wrapper"]}>
                        <div className={style["submit-button"]}
                            onClick={handleSubmit}
                        >
                            {TEXT.submitButton}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
