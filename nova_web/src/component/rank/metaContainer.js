import { useEffect, useState } from "react";
import MetaPresenter from "./metaPresenter";

function MetaContainer({ type, index }) {
    const [leagues, setLeagues] = useState([]);
    const [rankData, setRankData] = useState([]);

    const url = "http://nova-platform.kr/home";

    const fetchData = async () => {
        try {
            const firstResponse = await fetch(url + "/league_data?league_type=" + type);
            if (!firstResponse.ok) throw new Error('First fetch failed');
            const firstResult = await firstResponse.json();
            await setLeagues(firstResult.body.leagues);
            //console.log(firstResult.body)
        } catch (err) {
            console.log(err.message);
        }
    };

    useEffect(() => {
        const fetchData2 = async () => {
        try {
            const secondResponse= await fetch(url + "/show_league?league_name="
                + leagues[index].lname);
            if (!secondResponse.ok) throw new Error('Second fetch failed');
            const secondResult = await secondResponse.json();
            setRankData(secondResult.body.rank);
        } catch (err) {
            console.log(err.message);
        } 
    };

    fetchData2();
  }, []);

    fetchData();

    return <MetaPresenter rank={rankData} leagues={leagues} index={index} type={type} />;
}

export default MetaContainer;
