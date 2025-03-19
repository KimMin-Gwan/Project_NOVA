import "./index.css";
import sample from "./../../img/chzzz.svg";
import { BIAS_URL } from "../../constant/biasUrl";
export default function FollowBiasModal({ closeModal }) {
  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="streamer-img">
          <img src={sample} alt="프로필 이미지" />
          {/* <img src={BIAS_URL + `${clickedBid}.PNG`} /> */}
        </div>

        <p>
          이시연님을 <b>팔로우</b>
          합니다
        </p>
        <span>
          <button onClick={closeModal}>취소</button>
          <button className="follow-button">팔로우</button>
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
//           {clickedBname}님을{" "}
//           <b>
//             {biasList.some((item) => {
//               return item.bid === clickedBid;
//             })
//               ? "팔로우 취소"
//               : "팔로우"}
//           </b>
//           합니다
//         </p>
//         <span>
//           <button className={style["follow-button"]} onClick={fetchTryFollowBias}>
//             {biasList.some((item) => {
//               return item.bid === clickedBid;
//             })
//               ? "팔로우 취소"
//               : "팔로우"}
//           </button>
//         </span>
//       </div>
//     </div>
// }
