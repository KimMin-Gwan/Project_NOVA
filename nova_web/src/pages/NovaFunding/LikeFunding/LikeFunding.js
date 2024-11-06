import style from "./LikeFunding.module.css";
import backword from "./../../../img/back_icon.png";
import { useNavigate } from "react-router-dom";
export default function LikeFunding() {
  let navigate = useNavigate();

  function handleLinkClick(url) {
    navigate(url);
  }

  return (
    <div className={style.container}>
      <header className={style.Topbar}>
        <img src={backword} alt="Arrow" className={style.backword} onClick={() => handleLinkClick(-1)} />
        <div className={style.title}>자세히</div>
        <div className={style.EmptyBox} />
      </header>

      <section className={style.artist_info}>
        <div className={style.artist_img}>이미지</div>
        <section className={style.info}>
          <div className={style.artist_nav}>
            <div>이미지</div>
            <h3>언네임</h3>
            <button>자세히</button>
          </div>
          <div className={style.hashtag_box}>
            <span>#해시태그</span>
            <span>#해시태그</span>
          </div>
          <hr></hr>
          <div className={style.artist_exp}>
            <h4>[데뷔 앨범] 언네임 신곡 앨범 펀딩</h4>
            <div className={style.exp_text}>
              진용진님의프로젝트로 인기를 끌었던 데뷔조의 3인방이 언네임으로 돌아옵니다. <br></br>
              진짜 아이돌이 되어 여러분의 가슴을 뜨겁게 만들어줄 언네임의앨범을 가장 먼저 만나보세요!
            </div>
          </div>
          <div className={style.funding_condition}>
            <p>120명 참여</p>
            <span>별별티켓 400,000개 달성</span>
          </div>
        </section>
        <hr />
      </section>

      <div className={style["grid-container"]}>
        <div className={style["grid-item"]}>수령방법</div>
        <div className={style["grid-item"]}>택배</div>
        <div className={style["grid-item"]}>혜택</div>
        <div className={style["grid-item"]}>쇼케이스 자동응모</div>
      </div>
      <div className={style["product-box"]}>상품 소개 페이지</div>
    </div>
  );
}