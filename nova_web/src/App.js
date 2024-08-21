import './App.css';
import { useEffect, useState } from 'react';
import Banner from './component/banner';
import Modal from './component/modal';
import MyBias from './Container/myBiasContainer';
import MyPage from './pages/Mypage';
import { Routes, Route, Link } from 'react-router-dom';
import zoom from './img/zoom.png';
import menu from './img/menu.png';
import Rank from './component/ranks';
import FloatingButton from './component/floatingbutton';
import Meta from './Container/metaContainer';
import Loundspeaker from './component/loundspeaker';
import NOVALogin from './pages/NovaLogin/NovaLogin';

function App() {

  let url = 'http://nova-platform.kr/home/';
  let type = ['solo', 'group'];

  let header = {
    "request-type": "default",
    "client-version": 'v1.0.1',
    "client-ip": '127.0.0.1',
    "uid": '1234-abcd-5678',
    "endpoint": "/core_system/",
  }

  let jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzk5NDMzMCwiZXhwIjoxNzIzOTk2MTMwfQ.PWzlMUMKjMrgxc8Yl59-eIQPLP0QasunTnNl487ZWMA'

  let select_bias_send_data = {
    "header": header,
    "body": {
      'token': jwt,
      'bid': 1001,
    }
  }


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
        console.log('app화면')
        
        
      })
  }, [url])

  let [rank, setRank] = useState([]);
  let rank_copy = [];
  let profile_url = 'https://kr.object.ncloudstorage.com/nova-images/';

  //내 최애 / 전체 선택버튼용
  let [isClicked, setClick] = useState(false);
  let [isGroupClicked, setGroupClick] = useState(false);

  let [isTouched, setTouched] = useState('전체');

  function handleTouch(value) {
    setTouched(value)
  };

  function handleSoloToggle() {
    setClick(!isClicked);
  };

  function handleGroupToggle() {
    setGroupClick(!isGroupClicked);
  };

  let [showBox, setShowBox] = useState(false);
  let [blackBox, setBlackBox] = useState();


  function backgroundBlack(){
    if(showBox)
    {
      setBlackBox('black-box');
    }
    else{
      setBlackBox('');
    }
  };



  return (
    <Routes>
      <Route path='/mypage' element={<MyPage />}></Route>
      <Route path='/novalogin' element={<NOVALogin />}></Route>
      <Route path='/' element={
        <div onClick={() => {
          if (showBox)
            {
              setShowBox(false);
            };
        }} className={`container ${blackBox}`}>

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
                <Link to='/mypage' className='button'>마이페이지</Link>
                {/* <Link to='/mybias' className='button'>최애페이지</Link> */}
              </div>
            </header>
            <Banner></Banner>

            <h2 className='authen'>인증하기</h2>


            <section className='my-bias'>
              <MyBias url={url}></MyBias>
            </section>
          </div>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">개인리그 랭킹</div>
              <div className={`toggle-container ${isClicked ? "" : "active"}`}>
                <div onClick={() => {
                  handleSoloToggle()
                  handleTouch('내 최애')
                }} className={`text ${isClicked ? "" : "active"}`}>내 최애</div>
                <div onClick={() => {
                  handleSoloToggle()
                  handleTouch('전체')
                }} className={`text ${isClicked ? "active" : ""}`}>전체</div>
                <div className="toggle-slider"></div>

              </div>
            </div>
            <Meta url={url} isClicked={isClicked} type={type[0]}></Meta>

          </section>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">단체리그 랭킹</div>
              <div className={`toggle-container ${isGroupClicked ? "" : "active"}`}>
                <div onClick={() => {
                  handleGroupToggle()
                  handleTouch('내 최애')
                }} className={`text ${isGroupClicked ? "" : "active"}`}>내 최애</div>
                <div onClick={() => {
                  handleGroupToggle()
                  handleTouch('전체')
                }} className={`text ${isGroupClicked ? "active" : ""}`}>전체</div>
                <div className="toggle-slider"></div>

              </div>
            </div>
            <Meta url={url} isClicked={isGroupClicked} type={type[1]}></Meta>
          </section>

          <section className="advise"></section>
          <FloatingButton showSpeaker={showBox} setShowSpeaker={setShowBox}></FloatingButton>
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