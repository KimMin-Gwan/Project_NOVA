import style from "./error_page.module.css";

export default function NotYet(){
    return(
        <div className={style["screen"]}>
            <div className={style["text-wrapper"]}>
                <span className={style["span"]}> 스트리밍 컨텐츠 공유는 슈퍼노바</span>
                <span className={style["middle"]}> SUPERNOVA </span>
                <span className={style["span"]}> 아직 준비중 입니다.</span>
                <span className={style["span2"]}> 문의 - alsrhks2508@naver.com</span>
            </div>
        </div>
    )
}
   