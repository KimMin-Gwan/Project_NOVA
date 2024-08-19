import { useEffect, useState } from "react";
import RankPresenter from "./rankPresenter";
import MetaContainer from "./metaContainer";

const MetaPresenter = ({ rank, leagues, index, type }) => {

    return(
        <div>
        <div className="stars">
            {
                leagues.map(function (b, i) {
                    return (
                        <div className='행성 ' key={i}>
                        <button onClick={() => {
                            <MetaContainer meta={type} index={i}></MetaContainer>
                        }} className={index=== i ? 'click-now' : 'non-click'} click>{leagues[i]}</button>
                        </div>
                    );
                })
            }
        </div>
            <div className ="league">
                <RankPresenter rank={rank}></RankPresenter>
            </div>
        </div>
    );
}
export default MetaPresenter;