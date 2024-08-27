import { useEffect, useState } from "react";
import { BsDot } from "react-icons/bs";
import Ranks from "./ranks";



function League({ url, leagues, isClicked }) {

    let [rank, setRank] = useState([]);
    let [biasRank, setBiasRank] = useState([]);

    let [myBiasIndex, setMyBiasIndex] = useState(0);

    // let rank_copy = [];
    let [clickedIndex, setClickedIndex] = useState(0);
    // let [showIcon, setShowIcon] = useState(true);

    // function dotIconShow(){
    //     setShowIcon(true);
    // }

    useEffect(() => {
        const fetchData = async () => {
            try {
                const league = leagues[clickedIndex];
                const response = await fetch(url + `show_league?league_name=${league}`);
                const data = await response.json();
                setRank(data.body.rank);
                // console.log(2);
                console.log('랭킹 데이터 :', leagues);


            }
            catch (error) {
                console.error('Error fetching data: ', error);

            }
        };
        fetchData();

        if (isClicked) {
            return setClickedIndex(0)
        }
    }, [url, clickedIndex, leagues, isClicked]);

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
                                    } className={clickedIndex === i ? 'click-now' : 'non-click'}>{leagues[i]}
                                    </button>
                                    {
                                        clickedIndex === i && (
                                            <div className="icon-box">
                                                <BsDot className="icon" />
                                            </div>
                                        )
                                    }
                                </div>
                            );
                        }
                        else if (isClicked) {
                            return (
                                <div className='행성 ' key={i}>
                                    <button onClick={() => {
                                        setClickedIndex(0);
                                    }
                                    } className={'click-now'}>{leagues[i]}</button>
                                    {
                                        (
                                            <div className="icon-box">
                                                <BsDot className="icon" />
                                            </div>
                                        )
                                    }
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