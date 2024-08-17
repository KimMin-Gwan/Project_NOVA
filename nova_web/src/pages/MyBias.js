import { Routes, Route, Link } from 'react-router-dom'

function MyBias() {
    return (
        <div>
            <div>최애 페이지</div>
            <Link to='/' className='button'>홈</Link>
        </div>
    )
}

export default MyBias;