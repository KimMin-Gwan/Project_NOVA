import mainApi from "../../services/apis/mainApi";


export function formatDateTime(dateStr) {
  const date = new Date(dateStr);

  // 날짜
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  // 요일
  const weekDays = ["일", "월", "화", "수", "목", "금", "토"];
  const week = weekDays[date.getDay()];

  const formattedDate = `${month}월 ${day}일 ${week}`;

  // 시간
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const ampm = hours >= 12 ? "오후" : "오전";
  hours = hours % 12;
  hours = hours ? hours : 12; // 0 -> 12
  const formattedTime = `${ampm} ${String(hours).padStart(2,"0")}:${minutes}`;

  return { formattedDate, formattedTime };
}

export const fetchSubscribeSchedule = async (sid, setSubscribe) => {
  try {
    const res = await mainApi.get(`/time_table_server/try_subscribe_schedule?sid=${sid}`);
    setSubscribe((prev) => !prev);
    return true;
  } catch (err) {
    if (err.response && err.response.status === 401) {
      return false;
    } else {
      console.error("요청 중 오류 발생:", err);
      return false;
    }
  }
};

