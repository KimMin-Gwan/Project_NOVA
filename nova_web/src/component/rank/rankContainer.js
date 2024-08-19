import { useEffect, useState } from "react";
import RankPresenter from "./rankPresenter";

function RankContainer({lname}) {
    const [rankData, setRankData] = useState([]);

    let url = "http://nova-platform.kr/home"

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response= await fetch(url + "/home/show_league?league_name=" + lname);
        if (!response.ok) throw new Error('Second fetch failed');
        const result = await response.json();
        setRankData(result.body.rank);
      } catch (err) {
        console.log(err.message);
      } 
    };
    fetchData();
  }, []);

  return <RankPresenter rank={rank}></RankPresenter>
}

export default RankContainer;