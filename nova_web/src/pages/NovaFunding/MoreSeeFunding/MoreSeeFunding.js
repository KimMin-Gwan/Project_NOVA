import style_sub from "./../DuckFunding/DuckFunding.module.css";
import style from "./MoreSeeFunding.module.css";
import backword from "./../../../img/back_icon.png";
import test from "./../../../img/galaxyleague.png";
import { useNavigate } from "react-router-dom";
import Slider from "react-slick";

export default function MoreSeeFunding() {
  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 6, // 슬라이드 6개씩 표시
    slidesToScroll: 1,
    arrows: false,
  };

  const numberOfBoxes = 6;
  const boxes = [];

  for (let i = 1; i <= numberOfBoxes; i++) {
    boxes.push(
      <div className={style["new-list"]} key={i}>
        박스 {i}
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
        <img src={backword} alt="Arrow" className={style_sub.backword} onClick={() => handleLinkClick(-1)} />
        <section className={style["new-box"]}>
          <h3>7UCKY 7종 세트 </h3>
          <p>안녕하새오, 저는 람쥐 러낀대오 드디어 단독 한정판 러끼 굿즈가 오픈! 반년동안 러버들 몰래 준비하느라 진땀뺐다!</p>
          <button onClick={() => handleLinkClick("/details")}>상세정보</button>
        </section>
      </header>

      <div className={style.SliderContainer}>
        <Slider {...settings} className={style.Slider}>
          {boxes}
        </Slider>
      </div>
    </div>
  );
}
