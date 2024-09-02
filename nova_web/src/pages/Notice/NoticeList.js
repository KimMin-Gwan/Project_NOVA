import { Link, useNavigate } from 'react-router-dom';
import style from './NoticeList.module.css';

function NoticeList(){

    let navigate = useNavigate();

    return (
        <div className={style['main-body']}>
            <div className={style['top-area']}>공지사항</div>
            <div className={style['notice-area']}>
                <div className={style.notice} onClick={()=>{navigate('/notice')}}>공지사항 1</div>
                <div className={style.notice} onClick={()=>{navigate('/notice')}}>공지사항 2</div>
                <div className={style.notice} onClick={()=>{navigate('/notice')}}>공지사항 3</div>
            </div>
        </div>
    )
}

export default NoticeList;