import { Routes, Route, Link } from 'react-router-dom'

function MyPage() {
    return (
        <div>
            <div>마이페이지</div>
            <Link to='/' className='button'>홈</Link>
        </div>
    )
}

export default MyPage;