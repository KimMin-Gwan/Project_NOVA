import { duration } from "@mui/material/styles";
import style from "./BiasPage.module.css";
import mainApi from "../../services/apis/mainApi";

const biasState = {
    "TEMP": "임시 등록 상태",
    "CONFIRMED": "등록 완료 상태",
    "PRO": "슈퍼노바 파트너"
};

export const getBiasStateStr = (state) => {
    return biasState[state] || "알 수 없는 상태";
};

export const getStartTime = (datetime) => {
    const date = new Date(datetime);
    let hours = date.getHours(); // 0~23
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";

    // 24시간 → 12시간
    hours = hours % 12;
    if (hours === 0) hours = 12;

    // 2자리 숫자로 포맷
    const strHours = String(hours).padStart(2, "0");
    const strMinutes = String(minutes).padStart(2, "0");

    return `${ampm} ${strHours}:${strMinutes}`;
};

export const getEndTime = (datetime, duration) => {
    const date = new Date(datetime);

    // duration 시간 더하기
    date.setHours(date.getHours() + duration);

    // AM/PM 변환
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";

    hours = hours % 12;
    if (hours === 0) hours = 12;

    const strHours = String(hours).padStart(2, "0");
    const strMinutes = String(minutes).padStart(2, "0");

    return `${ampm} ${strHours}:${strMinutes}`;
};

export const handlePreviewImage = (url, setImage) => {
    const cacheBuster = Date.now(); // 캐시 방지용
    const urlWithCacheBuster = `${url}?cb=${cacheBuster}`;

    const img = new Image();
    img.src = urlWithCacheBuster;

    img.onload = () => {
        setImage(urlWithCacheBuster); // 캐시 방지 URL로 상태 세팅
    };

    img.onerror = () => {
        setImage(null);
    };
};

export const defaultImage = "https://kr.object.ncloudstorage.com/nova-images/no-image.png";

export const ToggleSwitch = ({id, isChecked, handleChecked}) => {
  const handleToggle = (e) => {
    handleChecked(e.target.checked);
  };

  return (
    <div className={style["toggleSwitchWrapper"]}>
      <input
        type="checkbox"
        id={id}
        hidden
        checked={isChecked}
        onChange={handleToggle}
      />
      <label htmlFor={id} className={style["toggleSwitch"]}>
        <span className={style["toggleButton"]}></span>
      </label>
    </div>
  )
}

export const fetchIsValidUser = async (bid) => {
  const res = await mainApi.get(`/nova_sub_system/is_valid_bias?bid=${bid}`)

  if(res.data.body.result){
    return true
  }else{
    return false
  }
}

export const fetchChangeBiasIntro = async (bid, intro) => {
  const res = await mainApi.get(`/nova_sub_system/modify_bias_introduce?bid=${bid}&introduce=${intro}`)

  if(res.data.body.result){
    return true
  }else{
    return false
  }
}

export const fetchChangeBiasUploadMode = async (bid, nowState) => {
  const res = await mainApi.get(`/nova_sub_system/change_open_content_mode?bid=${bid}&open_content_mode=${nowState}`)

  if(res.data.body.result){
    return true
  }else{
    return false
  }
}


export const handleFileChange = (event, bid, setImage) => {
  const formData = new FormData();
  const file = event.target.files[0];
  formData.append("image", file);

  if (file) {
    const imageUrl = URL.createObjectURL(file);
    setImage(imageUrl);
  }

  fetch(`https://supernova.io.kr/nova_sub_system/try_change_bias_profile_photo?bid=${bid}`, {
    method: "POST",
    credentials: "include",
    body: formData,
  })
    .then((res) => {
      res.json();
    })
    .then((data) => {
      alert("완료");
      window.location.reload();
    })
    .catch((error) => {
      alert("실패");
    });
};


