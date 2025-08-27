import style from "./error_page.module.css";

export default function ErrorPage(){
    return(
        <div className={style["screen"]}>
            <div className={style["text-wrapper"]}>
                <span className={style["span"]}> 여기가 어디죠?</span>
                <span className={style["middle"]}> 404 ERROR</span>
                <span className={style["span"]}> 찾는 곳이 여기는 아닌가 봅니다</span>
            </div>
        </div>
    );
}