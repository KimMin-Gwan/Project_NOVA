import { useNavigate } from 'react-router-dom';
import style from './../Mypage.module.css';

export default function MyInterestFeed(){
    let navigate = useNavigate();

    return (
        <div className='container'>
            <div className='top_area'>
                <div onClick={() => { navigate(-1) }}>뒤로</div>
                <div>은하계 탐색</div>
            </div>
        </div>
    )
}