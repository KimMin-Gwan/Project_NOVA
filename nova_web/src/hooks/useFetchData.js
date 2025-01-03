import { useEffect, useState } from "react";

// 홈 화면 fetch 받기
export default function useFetchData(url) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  async function fetchData() {
    await fetch(url, { credentials: "include" })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        console.log(`data ${url}`, data.body.send_data);
        setData(data.body.send_data);
        setLoading(false);
      });
  }

  useEffect(() => {
    fetchData();
  }, []);

  return data;
}
