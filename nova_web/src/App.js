import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import Banner from './component/banner';
import Modal from './component/modal';
import MyBias from './Container/myBiasContainer';
import MyPage from './pages/Mypage';
import { Routes, Route, Link } from 'react-router-dom';
import zoom from './img/zoom.png';
import menu from './img/menu.png';
import plus from './img/plus.png';
import empty from './img/empty.png';
import icon from './img/Icon.png';

import Rank from './component/rank';
import FloatingButton from './component/floatingbutton';
import EmptyBias from './component/subscribeBias/myGroupBias';
import SupportBias from './component/subscribeBias/mySoloBias';

// bid = ''가 이거면 오른쪽 레이아웃 바둑판

function App() {

  let url = 'http://175.106.99.34/home/';

  let bias_url = url + 'my_bias';
  let my_bias_url = 'https://kr.object.ncloudstorage.com/nova-images/';

  let [bias, setBias] = useState([]);
  let [group_bias, setGroupBias] = useState([]);

  let bias_copy = [];
  let group_bias_copy = [];

  let header = {
    "request-type": "default",
    "client-version": 'v1.0.1',
    "client-ip": '127.0.0.1',
    "uid": '1234-abcd-5678',
    "endpoint": "/core_system/",
  }

  let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzk5NDMzMCwiZXhwIjoxNzIzOTk2MTMwfQ.PWzlMUMKjMrgxc8Yl59-eIQPLP0QasunTnNl487ZWMA'

  let send_data = {
    "header": header,
    "body": {
      'token': jwt
    }
  }

  let select_bias_send_data = {
    "header": header,
    "body": {
      'token': jwt,
      'bid': 1001,
    }
  }

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
        group_bias_copy = data.body.group_bias;
        // console.log(group_bias_copy);
        setBias(bias_copy);
        setGroupBias(group_bias_copy);
      })
  }, [bias_url])

  let [leagues, setLeague] = useState([]);
  let league_copy = [];


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

  //내 최애 / 전체 선택버튼용
  let [isClicked, setClick] = useState(false);
  let [isClicked2, setClick2] = useState(false);

  let [isTouched, setTouched] = useState('전체');

  function handleTouch(value) {
    setTouched(value)
  };

  function handleToggle() {
    setClick(!isClicked);
  };

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

            <h2 className='authen'>인증하기</h2>


            <section className='my-bias'>
              <MyBias></MyBias>
              {/* <SupportBias></SupportBias>
              {/* <MyBias></MyBias> */}
              {/* <EmptyBias></EmptyBias> */}
            </section>
          </div>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">개인리그 랭킹</div>
              <div className={`toggle-container ${isClicked ? "" : "active"}`}>
                <div onClick={() => {
                  handleToggle()
                  handleTouch('내 최애')
                }} className={`text ${isClicked ? "" : "active"}`}>내 최애</div>
                <div onClick={() => {
                  handleToggle()
                  handleTouch('전체')
                }} className={`text ${isClicked ? "active" : ""}`}>전체</div>
                <div className="toggle-slider"></div>

              </div>
            </div>
            <div className="stars">
              {
                leagues.map(function (b, i) {
                  if (isTouched === '전체') {
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

            <div className="league">
              <Rank rank={rank} clicked={isTouched}></Rank>
            </div>
            {/* {
                rank.map(function (a, i) {
                  if (isTouched === '전체') {
                    return (
                      <div className="rank-item-box" key={i}>
                        <div className="rank-profile">
                          <img src={profile_url + `${rank[i].bid}.PNG`}></img>
                        </div>
                        <div className="name">{rank[i].bname}</div>
                        <div className="point">{rank[i].point} pt  
                          <img src={icon}></img>
                        </div>
                      </div>
                    )
                  }
                })
              } */}
          </section>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">단체리그 랭킹</div>
              <div className={`toggle-container ${isClicked ? "" : "active"}`}>
                <div onClick={() => {
                  handleToggle()
                  handleTouch('내 최애')
                }} className={`text ${isClicked ? "" : "active"}`}>내 최애</div>
                <div onClick={() => {
                  handleToggle()
                  handleTouch('전체')
                }} className={`text ${isClicked ? "active" : ""}`}>전체</div>
                <div className="toggle-slider"></div>

              </div>
            </div>
            <div className="stars">
              {
                leagues.map(function (b, i) {
                  if (isTouched === '전체') {
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

            <div className="league">
              <Rank rank={rank} clicked={isTouched}></Rank>
            </div>
          </section>

          <section className="advise"></section>
          <FloatingButton></FloatingButton>
          <footer className="footer">
            <div>
              <p>사업명 및 다양한 정보를 etc...</p>
              <p>주소: 부산 어딘가</p>
              <p>전화번호: 010-0000-000</p>
            </div>
            <div className="loundspeaker">
              {/* <button>확성기</button> */}
            </div>

          </footer>
        </div >


      } />

    </Routes>
  );
}

export default App;