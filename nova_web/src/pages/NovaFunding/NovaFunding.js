import style from "./NovaFunding.module.css";
import logo from "./../../img/NOVA.png";
import menu from "./../../img/menu-burger.png";
import more_icon from "./../../img/back.png";
import { useNavigate } from "react-router-dom";
export default function NovaFunding() {
  let navigate = useNavigate();
  return (
    <div className={style.container}>
      <header className={style.header}>
        <div className="logo">
          <img src={logo} alt="logo"></img>
        </div>
        <div className="buttons">
          <button className="tool-button">
            <img
              src={menu}
              alt="menu"
              onClick={() => {
                navigate("/more_see");
              }}
            ></img>
          </button>
        </div>
      </header>
      <div className={style["img-box"]}>
        이미지박스
        <div className={style["arrow-icon"]}>화살표</div>
      </div>
      <section className={style["recommend-box"]}>
        <div className={style["title-box"]}>
          <h2 className={style["title-text"]}>이런 펀딩 프로젝트는 어때요?</h2>
          <img src={more_icon} className={style["more-icon"]}></img>
        </div>
        <p className={style["more-text"]}>해시 태그로 찾아보는 펀딩 프로젝트</p>
        <div className={style["tag-container"]}>
          <button className={style["hashtag-text"]}># 시연</button>
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

      <section className={style["best-funding"]}>
        <div className={style["best-title"]}>
          <div className={style["top-title"]}>
            <h4>진행 중인 최애펀딩</h4>
            <a>더보기</a>
          </div>
          <p>최애가 직접 만드는 펀딩 프로젝트</p>
        </div>
        <div className={style["funding-main"]}>
          <div className={style["album-area"]}>
            <div className={style["album-img"]}>앨범표지</div>
            <p>신인 남자 아이돌 [언네임] 1집 앨범 펀딩</p>
          </div>
          <div className={style["more-container"]}>
            <p>별별 티켓 | 180,000개</p>
            <p>펀딩 가능 기간 | 24/05/16 까지</p>
            <p>87,500개 투자됨</p>
            <div className={style["progress-bar"]}>
              <progress value="70" max="100"></progress>
              <p>70%</p>
            </div>
            <button>자세히보기</button>
          </div>
        </div>
      </section>

      <section className={style["recommend-box"]}>
        <div className={style["title-box"]}>
          <h2 className={style["title-text"]}>베스트 프로젝트 모두 보기</h2>
        </div>
        <p className={style["more-text"]}>지금까지 펀딩된 프로젝트와 투자자들을 알아봐요!</p>

        <div className={style["ad-container"]}>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

            <p>72% 달성했어요</p>
          </div>
        </div>
      </section>

      <section className={style["open-funding"]}>
        <div className={style["best-title"]}>
          <div className={style["top-title"]}>
            <h4>진행 중인 오픈펀딩</h4>
            <a>더보기</a>
          </div>
          <p>누구나 팬 활동을 다같이 하고 싶다면!</p>
          <ul className={style["open-container"]}>
            <li className={style["open-box"]}>
              <div className={style["open-img"]}>이미지</div>
              <div className={style["text-area"]}>
                <div className={style["who-text"]}>
                  <h4>이시연 생일 카페 펀딩</h4>
                  <p>바위게</p>
                </div>
                <footer className={style["footer-line"]}>
                  <time>24/10/12까지</time>
                  <button>자세히 보기</button>
                </footer>
              </div>
            </li>
            <li className={style["open-box"]}>
              <div className={style["open-img"]}>이미지</div>
              <div className={style["text-area"]}>
                <div className={style["who-text"]}>
                  <h4>이시연 생일 카페 펀딩</h4>
                  <p>바위게</p>
                </div>
                <footer className={style["footer-line"]}>
                  <time>24/10/12까지</time>
                  <button>자세히 보기</button>
                </footer>
              </div>
            </li>
            <li className={style["open-box"]}>
              <div className={style["open-img"]}>이미지</div>
              <div className={style["text-area"]}>
                <div className={style["who-text"]}>
                  <h4>이시연 생일 카페 펀딩</h4>
                  <p>바위게</p>
                </div>
                <footer className={style["footer-line"]}>
                  <time>24/10/12까지</time>
                  <button>자세히 보기</button>
                </footer>
              </div>
            </li>
            <li className={style["open-box"]}>
              <div className={style["open-img"]}>이미지</div>
              <div className={style["text-area"]}>
                <div className={style["who-text"]}>
                  <h4>이시연 생일 카페 펀딩</h4>
                  <p>바위게</p>
                </div>
                <footer className={style["footer-line"]}>
                  <time>24/10/12까지</time>
                  <button>자세히 보기</button>
                </footer>
              </div>
            </li>
            <li className={style["open-box"]}>
              <div className={style["open-img"]}>이미지</div>
              <div className={style["text-area"]}>
                <div className={style["who-text"]}>
                  <h4>이시연 생일 카페 펀딩</h4>
                  <p>바위게</p>
                </div>
                <footer className={style["footer-line"]}>
                  <time>24/10/12까지</time>
                  <button>자세히 보기</button>
                </footer>
              </div>
            </li>
          </ul>
        </div>
      </section>

      <section className={style["notice-nova"]}>
        <div className={style["title-box"]}>
          <h2 className={style["title-text"]}>노바 펀딩 알아보기</h2>
          <img src={more_icon} className={style["more-icon"]}></img>
        </div>
        <p className={style["more-text"]}>30초만에 알아보는 노바 펀딩</p>

        <div className={style["ad-container"]}>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

            <p>72% 달성했어요</p>
          </div>
          <div className={style["ad-box"]}>
            <div className={style["img"]}>이미지</div>
            <p className={style["ad-title"]}>프로젝트 펀딩 순위</p>

            <p>72% 달성했어요</p>
          </div>
        </div>

        <div className={style["footer-area"]}>
          <div className={style["area-box"]}>참여한 펀딩</div>
          <div className={style["area-box"]}>
            펀딩 신청<br></br>
          </div>
        </div>

        <div className={style["last-project"]}>지난 펀딩 프로젝트</div>
      </section>
    </div>
  );
}
