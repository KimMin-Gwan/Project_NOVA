import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";

export default function useFetchData(url) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  async function fetchData() {
    try {
      const res = await mainApi.get(url);
      setData(res.data.body.send_data);
    } catch (error) {
      console.error("fetch error:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  return { data, loading };
}