import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import Banner from './component/banner';
import Modal from './component/modal';
import MyBias from './component/mybias';
import MyPage from './pages/Mypage';
import { Routes, Route, Link } from 'react-router-dom';
import zoom from './img/zoom.png';
import menu from './img/menu.png';
import plus from './img/plus.png';
import empty from './img/empty.png';
import SoloRank from './component/solo_rank';

// bid = ''가 이거면 오른쪽 레이아웃 바둑판

function App() {

  let [leagues, setLeague] = useState([]);
  let league_copy = [];
  let url = 'http://127.0.0.1:5000/home/';

  useEffect(() => {
    fetch(url + 'league_data?league_type=solo')
      .then(response => response.json())
      .then(data => {
        // league_copy = data.body.leagues[0].lname
        league_copy = data.body.leagues.map(leagues => leagues.lname);
        // console.log(JSON.stringify(league_copy));
        setLeague(league_copy);
      })
  }, [url])

  let [rank, setRank] = useState([]);
  let rank_copy = [];
  let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';

  let [isClicked, setClick] = useState('전체');

  function handleToggle(value) {
    setClick(value);
  }

  let [clickedIndex, setClickedIndex] = useState(0);

  return (
    <Routes>
      <Route path='/mypage' element={<MyPage />}></Route>
      <Route path='/mybias' element={<MyBias />}></Route>
      <Route path='/' element={
        <div className="container">
          <div className="top-area">
            <header className='header'>
              <div className='logo'>NOVA</div>
              <div className='buttons'>
                <button>
                  <img src={zoom}></img>
                </button>
                <button>
                  <img src={menu}></img>
                </button>
                {/* <Link to='/' className='button'>홈</Link> */}
                {/* <Link to='/mypage' className='button'>마이페이지</Link> */}
                {/* <Link to='/mybias' className='button'>최애페이지</Link> */}
              </div>
            </header>
            <Banner></Banner>

            <h2>인증하기</h2>

            
            <section className='my-bias'>
              <MyBias></MyBias>

              <div className='left-box'>
                <img src={empty}></img>
                {/* <div className='support'>지지하기</div> */}
                <div className='box'>
                  <div className='my-bias-group'>새로운 최애 그룹<br/>지지하기</div>
                  {/* <div className='bias-name'>{bias.bname}</div> */}
                </div>
                <button className='more'>
                  <img src={plus}></img>
                </button>
              </div>
            </section>
          </div>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">개인리그 랭킹</div>
              <div className='select-ranking'>
                <div onClick={() => handleToggle('내 최애')} className={isClicked === '내 최애' ? 'select-now' : 'select-not'}>내 최애</div>
                <div onClick={() => handleToggle('전체')} className={isClicked === '전체' ? 'select-now' : 'select-not'}>전체</div>
              </div>
            </div>
            <div className="stars">
              {
                leagues.map(function (b, i) {
                  if (isClicked === '전체') {
                    return (
                      <div className='행성 ' key={i}>
                        <button onClick={() => {
                          fetch(url + `show_league?league_name=${[leagues[i]]}`)
                            .then(response => response.json())
                            .then(data => {
                              rank_copy = [...data.body.rank]
                              setRank(rank_copy);
                              setClickedIndex(i);
                            })
                        }} className={clickedIndex === i ? 'click-now' : 'non-click'} click>{leagues[i]}</button>
                      </div>
                    );
                  }
                })
              }
            </div>
            
            {/* <SoloRank rank={rank}></SoloRank> */}
            <div className="league">
              {
                rank.map(function (a, i) {
                  if (isClicked === '전체') {
                    return (
                      <div className="rank-item-box" key={i}>
                        <div className='number'>{i + 1}.</div>
                        <div className="rank-profile">
                          <img src={profile_url + `${rank[i].bid}.PNG`}></img>
                        </div>
                        <div className="name">{rank[i].bname}</div>
                        <div className="point">1000pt</div>
                      </div>
                    )
                  }
                })
              }
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