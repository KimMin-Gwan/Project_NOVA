import "./index.css";
import sample from "./../../img/chzzz.svg";
import { BIAS_URL } from "../../constant/biasUrl";
import useBiasStore from "../../stores/BiasStore/useBiasStore";

export default function FollowBiasModal({ biasData, closeModal, fetchFollowBias }) {
  const { biasList } = useBiasStore();
  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="streamer-img">
          <img src={`${BIAS_URL}${biasData.bid}.PNG` || sample} alt="프로필 이미지" />
        </div>

        <p>
          {biasData.bname}님을{" "}
          <b>
            {biasList.some((item) => {
              return item.bid === biasData.bid;
            })
              ? "팔로우 취소"
              : "팔로우"}
          </b>
          합니다
        </p>

        <span>
          <button onClick={closeModal}>취소</button>
          <button
            className={"follow-button"}
            onClick={() => {
              fetchFollowBias(biasData.bid);
            }}
          >
            {biasList.some((item) => {
              return item.bid === biasData.bid;
            })
              ? "팔로우 취소"
              : "팔로우"}
          </button>
        </span>
      </div>
    </div>
  );
}

//         <button className={style["streamer-img"]}>
//           <div>
//             <img src={BIAS_URL + `${clickedBid}.PNG`} />
//           </div>
//         </button>
//         <p>
