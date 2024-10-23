import style from "./MainPart.module.css";

export default function IncreaseTag() {
    return (
        <div className={style['wrap-container']}>
            <div className={style['top-area']}>
                <div className={style["content-title"]}>
                    <header>급상승 해시태그</header>
                    {/* <div>화살표</div> */}
                </div>
            </div>

            <div className={style['main-area']}>
                <div className={style['hashtag-box']}>
                
                </div>
            </div>
        </div>
    )
}