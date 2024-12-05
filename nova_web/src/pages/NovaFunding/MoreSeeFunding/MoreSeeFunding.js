import style_sub from "./../DuckFunding/DuckFunding.module.css";
import style from "./MoreSeeFunding.module.css";
import backword from "./../../../img/back_icon.png";
import test from "./../../../img/galaxyleague.png";
import shadow from "./../../../img/shadow_funding.png";
import { useNavigate } from "react-router-dom";
import Slider from "react-slick";

export default function MoreSeeFunding() {
  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: false,
    focusOnSelect: true,
  };

  const numberOfBoxes = 6;
  const boxes = [];

  for (let i = 1; i <= numberOfBoxes; i++) {
    boxes.push(
      <div className={style["new-list"]} key={i}>
        <div className={style["new-img"]}>이미지</div>
        <div className={style["new-title"]}>
          <span>끠끠 첫 굿즈 출시!</span>
          <p>후원형</p>
        </div>
      </div>
    );
  }

  let navigate = useNavigate();

  function handleLinkClick(url) {
    navigate(url);
  }

  return (
    <div className={style_sub.container}>
      <header
        className={style.Topbar}
        style={{
          backgroundImage: `url(${test})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <img src={shadow} alt="Shadow Overlay" className={style.ShadowOverlay} />

        <img src={backword} alt="Arrow" className={`${style_sub.backword} ${style["backword"]}`} onClick={() => handleLinkClick(-1)} />
        <section className={style["new-box"]}>
          <h3>7UCKY 7종 세트 </h3>
          <p>안녕하새오, 저는 람쥐 러낀대오 드디어 단독 한정판 러끼 굿즈가 오픈! 반년동안 러버들 몰래 준비하느라 진땀뺐다!</p>
          <button onClick={() => handleLinkClick("/details")}>상세 정보</button>
        </section>
        <p className={style["new-fav"]}>신규 최애 펀딩 프로젝트</p>
      </header>
      <div className={style.SliderContainer}>
        <Slider {...settings}>{boxes}</Slider>
      </div>
      <section className={`${style_sub["success-funding"]} ${style["success-funding"]}`}>
        <div className={`${style_sub["content-title"]} ${style["content-title"]}`}>
          <header className={style_sub["header-text"]}>추천하는 프로젝트</header>
          <div onClick={() => handleLinkClick("/")}>전체보기</div>
        </div>

        <ul>
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
          <li>
            <div className={style["project-list"]}>
              <div className={style["pj-img"]}>이미지</div>
              <div className={style["pj-des"]}>
                <p>참여형</p>
                <h4>하꼬 버트버 키링 굿즈 제작 프로젝트</h4>
                <p>천유정</p>
                <p>12월 30일까지</p>
                <p>80% 달성</p>
                <button>상세정보</button>
              </div>
            </div>
          </li>
        </ul>
      </section>
    </div>
  );
}
