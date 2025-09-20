import HEADER from "../../constant/header";
import mainApi from "../../services/apis/mainApi";
import postApi from "../../services/apis/postApi";

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

export const formatKoreanDateTime = (date) => {
  if (!(date instanceof Date)) {
    return "";
  }

  // 요일 배열
  const days = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];

  const year = date.getFullYear();
  const month = date.getMonth() + 1; // 0부터 시작
  const day = date.getDate();
  const dayOfWeek = days[date.getDay()];

  let hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, "0");

  // 오전/오후 판별
  const ampm = hours >= 12 ? "오후" : "오전";
  hours = hours % 12 || 12; // 12시간제로 변환 (0시는 12시로)

  const dateStr = `${year}년 ${month.toString().padStart(2, "0")}월 ${day.toString().padStart(2, "0")}일 ${dayOfWeek}`;
  const timeStr = `${ampm} ${hours.toString().padStart(2, "0")}시 ${minutes}분`;

  return { dateStr, timeStr };
}

export const fetchScheduleData = async (sid) => {
  const res = await postApi.post('/time_table_server/get_schedule_with_sids', {
    header: HEADER,
    body: {
      sids: [sid]
    },
  });

  if (res.data.body.schedules[0]) return res.data.body.schedules[0]
  else return { sid: "" }
}

export const fetchSubscribeSchedule = async (sid) => {
  const res = await mainApi.post(`/time_table_server/try_subscribe_schedule?sid=${sid}`)

  return
}