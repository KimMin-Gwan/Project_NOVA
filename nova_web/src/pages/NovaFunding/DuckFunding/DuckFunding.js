import style from "./DuckFunding.module.css";
import backword from "./../../../img/back_icon.png";
import more_icon from "./../../../img/backword.png";

import { useNavigate } from "react-router-dom";
export default function DuckFunding() {
  let navigate = useNavigate();

  function handleLinkClick(url) {
    navigate(url);
  }

  return (
    <div className={style.container}>
      <header className={style.Topbar}>
        <img src={backword} alt="Arrow" className={style.backword} onClick={() => handleLinkClick(-1)} />   
        <div className={style.title}>덕질펀딩</div>
        <div className={style.EmptyBox} />
      </header>
     
      <section className={style["success-funding"]}>
       <div className={style["content-title"]}>
          <header className={style["header-text"]}>오늘의 베스트 피드</header>
          <div>전체보기</div>
        </div>

        <div className={style["best-container"]}>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
          <div className={style["best-box"]}>
            <div className={style["best-img"]}>이미지</div>
            <p className={style["best-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지 (1일 남음)</p>
            <p>72% 달성</p>
          </div>
         
        </div>


      </section>  

      <section className={style["success-funding"]}>
      <div className={style["content-title"]}>
          <header className={style["header-text"]}>마감임박 프로젝트</header>
          <div>전체보기</div>
        </div>

        <div className={style["ad-container"]}>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
        </div>
      </section>

   
      <section className={style["success-funding"]}>
      <div className={style["content-title"]}>
          <header className={style["header-text"]}>덕질 펀딩 프로젝트</header>
          
        </div>
      </section>

      <section className={`${style["success-funding"]} ${style["interest-funding"]}`}>
      <div className={style["content-title"]}>
          <header className={style["header-text"]}>마감임박 프로젝트</header>
          <div>전체보기</div>
        </div>
        <div className={style["ad-container"]}>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
        </div>
        <div className={style["ad-container"]}>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
        </div>
        <div className={style["ad-container"]}>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>이시연 생일 축하 학동역 광고</p>
            <p>24/10/26 일까지</p>
            <p>72% 달성했어요</p>
          </div>
        </div>


        <button className={style["more-button"]}>더보기</button>
      </section>

      
    </div>
  );
}
