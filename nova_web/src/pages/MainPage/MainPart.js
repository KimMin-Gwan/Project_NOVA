import style from './MainPart.module.css';

export default function MainPart(){
    return(
        <div className={style['wrap-container']}>
            <div className={style['top-area']}>
                <div className={style['content-title']}>
                    <div>[ 시연 ] 관련 인기 해시태그</div>
                    <div>화살표</div>
                </div>
                <div className={style['tag-container']}>버튼들</div>
            </div>
            
            <div className={style['main-area']}>
                <div className={style['feed-box']}>피드 박스</div>
            </div>
        </div>
    )
}