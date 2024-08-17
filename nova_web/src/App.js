import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import Banner from './component/banner';
import Modal from './component/modal';
import MyPage from './pages/Mypage';
import MyBias from './pages/MyBias';
import { Routes, Route, Link } from 'react-router-dom';
import zoom from './img/zoom.png';
import menu from './img/menu.png';
import plus from './img/plus.png';
import more from './img/more.png';

// bid = ''가 이거면 오른쪽 레이아웃 바둑판

function App() {

  let [leagues, setLeague] = useState([]);
  let league_copy = [];
  let url = 'http://127.0.0.1:80/home/';

  useEffect(() => {
    fetch(url + 'league_data?league_type=solo')
      .then(response => response.json())
      .then(data => {
        // league_copy = data.body.leagues[0].lname
        league_copy = data.body.leagues.map(leagues => leagues.lname);
        setLeague(league_copy);
      })
  }, [url])

  let [bias, setBias] = useState([]);
  let bias_copy = [];
  let header = {
    "request-type": "default",
    "client-version": 'v1.0.1',
    "client-ip": '127.0.0.1',
    "uid": '1234-abcd-5678',
    "endpoint": "/core_system/",
  }

  let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzkxNjE2NywiZXhwIjoxNzIzOTE3OTY3fQ.NnAH7uEV85D-J_T_5dZeuwP9-pRj8j794lNW0sa4YJs'

  let send_data = {
    "header": header,
    "body": {
      'token': jwt
    }
  }

  let bias_url = url + 'my_bias';
  let solo_bias = 'https://kr.object.ncloudstorage.com/cheese-images/';
  useEffect(() => {
    fetch(bias_url, {
      method: 'POST',
      headers: {
        "Content-Type": 'application/json',
      },
      body: JSON.stringify(send_data),
    })
      .then(response => response.json())
      .then(data => {
        bias_copy = data.body.solo_bias;
        setBias(bias_copy);
        // console.log(JSON.stringify(data.body.solo_bias))
      })
  }, [bias_url])

  let [rank, setRank] = useState([]);
  let rank_copy = [];
  let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';

  let rank_url = url + `show_league?league_name=${leagues}`;
  useEffect(() => {

    fetch(rank_url)
      .then(response => response.json())
      .then(data => {
        // rank_copy = [...data.body.rank].map()
        rank_copy = [...data.body.rank];
        setRank(rank_copy);
        // console.log(rank_copy.bname);
        // console.log(JSON.stringify([...rank_copy[0]][0].bname))
      })
  }, [rank_url])

  // false 일경우 전체
  let [my_or_all, setNow] = useState(false);
  let [select, setSelect] = useState('select-not');

  function selectChange() {
    if (my_or_all === false) {
      setNow('true');
      setSelect('select-not');
    }
    if (my_or_all === true) {
      setNow('false');
      setSelect('select-now');
    }
  }



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
                {/* <Link to='/' className='button'>홈</Link>
                <Link to='/mypage' className='button'>마이페이지</Link>
                <Link to='/mybias' className='button'>최애페이지</Link> */}
              </div>
            </header>
            <Banner></Banner>
            <h2>인증하기</h2>
            <section className='my-bias'>
              <div className='left-box'>
                <img src={solo_bias + `${bias.bid}.jpg`}></img>
                <div className='support'>지지하기</div>
                <button className='more'>
                  <img src={more}></img>
                </button>
              </div>
              <div className='left-box'>
                <img src={solo_bias + `${bias.bid}.jpg`}></img>
                <div className='support'>지지하기</div>
                <button className='more'>
                  <img src={more}></img>
                </button>
              </div>
            </section>
          </div>

          {/* <div class="toggle-container">
            <input type="radio" id="option1" name="toggle" checked />
            <label for="option1" class="toggle-label">내 최애</label>

            <input type="radio" id="option2" name="toggle" />
            <label for="option2" class="toggle-label">전체</label>

            <div class="toggle-slider"></div>
          </div> */}


          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">개인리그 랭킹</div>
              <div className='select-ranking'>
                <div onClick={selectChange} className={select}>내 최애</div>
                <div onClick={selectChange} className={select}>전체</div>
              </div>
            </div>
            <div className="stars">
              <button>{leagues}</button>
              <button>사수자리</button>
              <button>천칭자리</button>
              <button>물병자리</button>
              <button>전갈자리</button>
              <button>쌍둥이자리</button>
              <button>7</button>
              <button>8</button>
              <button>9</button>
              <button>10</button>
              {/* 눌리면 색 바뀌게
              버튼마다 내용다르게
                    */}
            </div>
            <div className="league">
              {
                rank.map(function (a, i) {
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