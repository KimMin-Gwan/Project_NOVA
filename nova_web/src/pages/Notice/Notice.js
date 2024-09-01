import style from './Notice.module.css';

function Notice(){
    return (
        <div className={style['main-body']}>
            <div className={style['top-area']}>공지사항</div>
            <div className={style['notice-area']}>
                <div className={style.notice}>공지사항 1</div>
                <div className={style.notice}>공지사항 1</div>
                <div className={style.notice}>공지사항 1</div>
            </div>
        </div>
    )
}

export default Notice;