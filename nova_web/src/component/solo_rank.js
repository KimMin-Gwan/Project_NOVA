import { useState, useEffect } from "react";

function SoloRank({ranks}) {
    let [rank, setRank] = useState([]);
    let rank_copy = [];
    let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';
    let [isClicked, setClick] = useState('전체');


    return (
        <div className="league">
            {
                rank.map(function (a, i) {
                    if (isClicked === '전체') {
                        return (
                            <div className="rank-item-box" key={i}>
                                <div className='number'>{i + 1}.</div>
                                <div className="rank-profile">
                                    <img src={profile_url + `${rank[i].bid}.PNG`}></img>
                                </div>
                                <div className="name">{rank[i].bname}</div>
                                <div className="point">1000pt</div>
                            </div>
                        )
                    }
                })
            }
        </div>
    )
}

export default SoloRank;