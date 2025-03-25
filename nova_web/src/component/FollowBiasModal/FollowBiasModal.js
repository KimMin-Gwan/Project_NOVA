import "./index.css";
import { BIAS_URL } from "../../constant/biasUrl";
import useBiasStore from "../../stores/BiasStore/useBiasStore";
import tempBias from "./../../img/tempBias.png";

export default function FollowBiasModal({ biasData, closeModal, fetchFollowBias }) {
  const { biasList } = useBiasStore();

  // 팔로우 상태 확인
  const isFollowed = biasList.some((item) => item.bid === biasData.bid);

  const handleFollowButton = () => {
    fetchFollowBias(biasData.bid);
  };

  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="streamer-img">
          <img
            src={BIAS_URL + `${biasData.bid}.PNG`}
            alt="bias"
            onError={(e) => {
              e.target.src = tempBias;
            }}
          />
        </div>

        <p>
          {biasData.bname}님을 <b>{isFollowed ? "팔로우 취소" : "팔로우"}</b>
          합니다
        </p>

        <span>
          <button onClick={closeModal}>취소</button>
          <button className={"follow-button"} onClick={handleFollowButton}>
            {isFollowed ? "팔로우 취소" : "팔로우"}
          </button>
        </span>
      </div>
    </div>
  );
}
