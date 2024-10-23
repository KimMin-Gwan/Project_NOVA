import style from "./MainPart.module.css";

export default function PopularFeed() {
    return (
        <div className={style['wrap-container']}>
            <div className={style['top-area']}>
                <div className={style["content-title"]}>
                    <header>최근 인기 게시글</header>
                    <div>화살표</div>
                </div>
            </div>

            <div className={style['main-area']}>
                <div className={style['popular-feed']}>
                    <div className={style['img-box']}>img</div>
                    <div>tag</div>
                    <div>글</div>
                </div>
            </div>
        </div>
    )
}