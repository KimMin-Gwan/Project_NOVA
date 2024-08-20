import { Routes, Route, Link } from 'react-router-dom'
import Loundspeaker from '../component/loundspeaker';

function MyPage() {


    return (
            // {/* <div className="toggle-container">
            //     <input type="radio" id="option1" name="toggle" checked />
            //     <label for="option1" className="toggle-label">내 최애</label>

            //     <input type="radio" id="option2" name="toggle" />
            //     <label for="option2" className="toggle-label">전체</label>

            //     <div className="toggle-slider"></div>
            // </div> */}
            
            <Loundspeaker></Loundspeaker>


            // {/* <div>마이페이지</div>
            // <Link to='/' className='button'>홈</Link> */}
    )
}

export default MyPage;