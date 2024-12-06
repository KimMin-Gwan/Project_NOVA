import style from "./LikeFunding.module.css";
import backword from "./../../../img/back_icon.png";
import { useNavigate } from "react-router-dom";
import nova_icon from "./../../../img/nova_icon.png";
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

      <section className={style["nova-platform-box"]}>
        <div className={style["box-title"]}>
          <img src={nova_icon}></img>
          <h3>노바 플랫폼에서 해당 펀딩을 이야기 해봐요!</h3>
        </div>
        <p className={style["nova_box-text"]}>
          #언네임 태그를 붙히며 숏피드를 작성해 보는 건 어떨까요??<br></br>혹시 모르죠..숨겨진 혜택이 있을지도!
        </p>

        <div className={style["button-container"]}>
          <button className={style["nova-button"]}>관련 글보기</button>
          <button className={style["nova-button"]} onClick={() => handleLinkClick("/")}>
            노바 플랫폼 바로가기
          </button>
        </div>
      </section>

      <section className={style["support_pj"]}>
        <p>후원 프로젝트</p>
        <div className={style["hold_ticket"]}>
          <div>
            <p>보유 별별 티켓</p>
            <input type="text" />개
          </div>
          <button>티켓 추가 구매</button>
        </div>
        <div className={style["hold_ticket"]}>
          <div>
            <p>이름</p>
            <input type="text" />
          </div>
          <div>
            <p>지원 금액</p>
            <input type="text" />개
          </div>

          <div className={style["button-style"]}>
            <button>지원내역</button>
            <button>지원하기</button>
          </div>
        </div>
      </section>
      <hr className={style["hr-style"]} />
      <section className={style["donater"]}>
        도네이터 목록
        <ul>
          <li>
            <p>40%</p>
            <p>닉네임1</p>
            <p>100,000원</p>
          </li>
          <li>
            <p>40%</p>
            <p>닉네임1</p>
            <p>100,000원</p>
          </li>
          <li>
            <p>40%</p>
            <p>닉네임1</p>
            <p>100,000원</p>
          </li>
          <li>
            <p>40%</p>
            <p>닉네임1</p>
            <p>100,000원</p>
          </li>
          <li>
            <p>40%</p>
            <p>닉네임1</p>
            <p>100,000원</p>
          </li>
          <li>
            <p>40%</p>
            <p>닉네임1</p>
            <p>100,000원</p>
          </li>
          <button>참여자 모두 보기</button>
        </ul>
      </section>

      <section className={style["support_pj"]}>
        <p>참여 프로젝트</p>
        <div className={style["hold_ticket"]}>
          <div>
            <p>보유 별별 티켓</p>
            <input type="text" />개
          </div>
          <button>티켓 추가 구매</button>
        </div>
        <div className={style["select_funding"]}>
          <div>
            <p>[얼리버드] 1집 데뷔 앨범</p>
            <p>600개 한정 수량</p>
            <p>1,300개</p>
          </div>
          <ul className={style["funding-list"]}>
            <li>
              언네임 데뷔앨범 1개
              <ul>
                <li>언네임 데뷔 특전 1세트</li>
              </ul>
            </li>
          </ul>
          <button>선택하기</button>
        </div>
        <div className={style["select_funding"]}>
          <div>
            <p>[얼리버드] 1집 데뷔 앨범</p>
            <p>600개 한정 수량</p>
            <p>1,300개</p>
          </div>
          <ul className={style["funding-list"]}>
            <li>
              언네임 데뷔앨범 1개
              <ul>
                <li>언네임 데뷔 특전 1세트</li>
              </ul>
            </li>
          </ul>
          <button>선택하기</button>
        </div>
      </section>
    </div>
  );
}
