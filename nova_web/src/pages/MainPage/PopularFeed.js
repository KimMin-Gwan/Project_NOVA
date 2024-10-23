import style from "./MainPart.module.css";

export default function PopularFeed() {
  return (
    <div className={style["wrap-container"]}>
      <div className={style["top-area"]}>
        <div className={style["content-title"]}>
          <header>최근 인기 게시글</header>
          <div>화살표</div>
        </div>
      </div>

      <div className={style["main-area"]}>
        <div className={style["popular-feed"]}>
          <div className={style["img-box"]}>img</div>
          <div className={style["popular-main"]}>
            <div className={style["tag-text"]}>
              <span className={style["tag"]}>#미츄</span>
              <span className={style["tag"]}>#아모몽</span>
              <span className={style["tag"]}>#미녕이</span>
            </div>
            <div className={style["popular-text"]}>이번 특별 박송은 진짜 개웃김 ㅋㅋㅋ 포스터에도 제갈금자 ㅇㅈㄹ ㅋㅋㅋㅋ 개웃기다 개웃겨요 글자가 벗어나게 하기 위해서 길게 글을 씁니다 이래도 안벗어나네 웃겨라 더 해야돼? ㅋㅋㅋㅋㅋㅋ</div>
          </div>
        </div>
      </div>
    </div>
  );
}
