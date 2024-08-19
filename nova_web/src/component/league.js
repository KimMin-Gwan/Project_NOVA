import { useEffect, useState } from "react";

import Ranks from "./ranks";



function League({ url, leagues, isClicked, biasLeague }) {

    let [rank, setRank] = useState([]);
    let [biasRank, setBiasRank] = useState([]);

    // let rank_copy = [];
    let [clickedIndex, setClickedIndex] = useState(0);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const league = leagues[clickedIndex];
                const response = await fetch(url + `show_league?league_name=${league}`);
                const data = await response.json();
                setRank(data.body.rank);
            }
            catch (error) {
                console.error('Error fetching data: ', error);
            }
        };
        fetchData();

    }, [clickedIndex, leagues]);

    return (
        <>
            <div className="stars">
                {
                    leagues.map(function (b, i) {
                        if (!isClicked) {
                            return (
                                <div className='행성 ' key={i}>
                                    <button onClick={() => {
                                        setClickedIndex(i);
                                    }
                                    } className={clickedIndex === i ? 'click-now' : 'non-click'}>{leagues[i]}</button>
                                </div>
                            );
                        }
                    })
                }
            </div>
            <Ranks rank={rank} isClicked={isClicked}></Ranks>
        </>
    )
}

export default League;