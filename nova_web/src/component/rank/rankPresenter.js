import React from 'react';
import icon from '../../img/Icon.png';

const RankPresenter = ({ rank }) => {

    let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';

    return (
        <div className="league">
            {
                rank.map(function (a, i) {
                    return (
                        <div className="rank-item-box" key={i}>
                            <div className="rank-profile">
                                <img src={profile_url + `${rank[i].bid}.PNG`}></img>
                            </div>
                            <div className="name">{rank[i].bname}</div>
                            <div className="point">{rank[i].point} pt
                                <img src={icon}></img>
                            </div>
                        </div>
                    )
                })
            }
        </div>
    )
};

export default RankPresenter;

