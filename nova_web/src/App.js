import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import Banner from './component/banner';
import Modal from './component/modal';
import MyPage from './pages/Mypage';
import MyBias from './pages/MyBias';
import { Routes, Route, Link } from 'react-router-dom'

function App() {

  return (
    <Routes>
      <Route path='/mypage' element={<MyPage />}></Route>
      <Route path='/mybias' element={<MyBias />}></Route>
      <Route path='/' element={
        <div className="container">
          <div className="top-area">
            <header className='header'>
              <div className='logo'>로고</div>
              <div className='buttons'>
                <Link to='/' className='button'>홈</Link>
                <Link to='/mypage' className='button'>마이페이지</Link>
                <Link to='/mybias' className='button'>최애페이지</Link>
              </div>
            </header>
            {/* 
        1. 시간이 지나면 자동으로 다음 베너로 넘어가도록
        2. 클릭 시 다음 베너로 넘어가도록
        3. 클릭 전 이미지 */}
            <Banner></Banner>


            <section className='my-bias'>
              <div className='left-box'>11</div>
              <div className='left-box'>11</div>
            </section>
          </div>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">개인리그 랭킹</div>
              <div className='select'>
                <div className='bias'>내 최애</div>
                <div onClick={() => {
                  fetch('http://127.0.0.1:80/home/league_data?league_type=solo')
                    .then(response => response.json())
                    .then(data => {
                      console.log(JSON.stringify(data));
                    })
                }} className='all-bias'>전체</div>
              </div>
            </div>
            <div className="stars">
              <button>오리온자리</button>
              <button>사수자리</button>
              <button>천칭자리</button>
              <button>물병자리</button>
              <button>전갈자리</button>
              <button>쌍둥이자리</button>
              <button>7</button>
              <button>8</button>
              <button>9</button>
              <button>10</button>
            </div>
            <h3>00리그</h3>
            <div className="league">
              <div className="rank-item-box">
                <div>1.</div>
                <div className="rank-profile"></div>
                <div className="name">이름</div>
                <div className="point">1000pt</div>
              </div>
              <div className="rank-item-box">
                <div>1.</div>
                <div className="rank-profile"></div>
                <div className="name">이름</div>
                <div className="point">1000pt</div>
              </div>
            </div>
          </section>

          <section className="advise"></section>

          <footer className="footer">
            <div>
              <p>사업명 및 다양한 정보를 etc...</p>
              <p>주소: 부산 어딘가</p>
              <p>전화번호: 010-0000-000</p>
            </div>
            <div className="loundspeaker">
              <button>확성기</button>
            </div>
          </footer>
        </div >
      } />

    </Routes>
  );
}

export default App;