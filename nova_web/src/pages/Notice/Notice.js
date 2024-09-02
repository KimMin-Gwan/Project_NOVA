import { Link } from 'react-router-dom';
import style from './NoticeList.module.css';

function Notice() {
    return (
        <div className={style['main-body']}>
            <div className={style['top-area']}>공지사항</div>
            <div className={style['notice-area']}>
                <div className={style.notice}>제목</div>
                <div className={style['png-area']}>공지사항 (png)</div>
            </div>
        </div>
    )
}

export default Notice;