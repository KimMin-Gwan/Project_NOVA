import style from "./ScheduleFollowBox.module.css";
import sample from "./../../img/chzzz.svg";
export default function ScheduleFollowBox({ closeModal }) {
  return (
    <div className={style["modal-overlay"]}>
      <div className={style["modal"]} onClick={(e) => e.stopPropagation()}>
        <div className={style["streamer-img"]}>
          <img src={sample} alt="프로필 이미지" />
        </div>

        <p>
          이시연님을 <b>팔로우</b>
          합니다
        </p>
        <span>
          <button onClick={closeModal}>취소</button>
          <button className={style["follow-button"]}>팔로우</button>
        </span>
      </div>
    </div>
  );
}
