import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";

// 홈 화면 fetch 받기
export default function useFetchData(url) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  async function fetchData() {
    await mainApi.get(url).then((res) => {
      setData(res.data.body.send_data);
      setLoading(false);
    });
  }

  useEffect(() => {
    fetchData();
  }, []);

  return data;
}
