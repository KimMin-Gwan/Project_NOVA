import './App.css';
import { useEffect, useState } from 'react';
import Banner from './component/banner';
import Modal from './component/modal';
import MyBias from './Container/myBiasContainer';
import MyPage from './pages/MyPage/Mypage';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
// import zoom from './img/zoom.png';
import menu from './img/menu.png';
// import Rank from './component/ranks';
// import FloatingButton from './component/floatingbutton';
// import Meta from './Container/metaContainer';
// import Loundspeaker from './component/loundspeaker';
import NOVALogin from './pages/NovaLogin/NovaLogin';
import SelectBias from './component/selectBias/SelectBias';
import BiasDetail from './pages/BiasDetail/biasDetail';
import BiasCertify from './pages/BiasCertify/biasCertify';
import NameCard from './pages/NameCard/nameCard';
import { FaSearch, IoMdMenu } from "react-icons/fa";
import MoreSee from './pages/MoreSee/MoreSee';
import NoticeList from './pages/Notice/NoticeList';
import Notice from './pages/Notice/Notice';
import LeaguePage from './pages/LeaguePage/LeaguePage';
import LeagueDetail from './pages/LeagueDetail/LeagueDetail';
import SignUp from './pages/SignUp/SignUp.js';
import FeedPage from './pages/FeedPage/FeedPage.js';
import Feed from './component/feed.js';
import InfFeed from './component/infiniteFeed.js';
import PlanetList from './pages/PlanetPage/PlanetList.js';
import logo from './img/NOVA.png';
import GalaxyList from './pages/GalaxyPage/GalaxyList.js';
import Box from './component/test.js';
import NavBar from './component/NavBar.js';


// 401 이면 바이어스 격자 무늬로 띄우기
// 401 이면 alert - 로그인 필요 문구 띄우기


function App() {

  let url = 'https://nova-platform.kr/home/';
  // let url = 'http://127.0.0.1:5000/home/';
  let type = ['solo', 'group'];


  let token = localStorage.getItem('jwtToken');
  
  let [isLogin, setIsLogin] = useState();
  let [newToken, setnewToken] = useState(token);

  let header = {
    "request-type": "default",
    "client-version": 'v1.0.1',
    "client-ip": '127.0.0.1',
    "uid": '1234-abcd-5678',
    "endpoint": "/core_system/",
  }

  //내 최애 / 전체 선택버튼용
  let [isSoloClicked, setSoloClick] = useState(false);
  let [isGroupClicked, setGroupClick] = useState(false);

  function handleSoloToggle() {
    setSoloClick(!isSoloClicked);
  };

  function handleGroupToggle() {
    setGroupClick(!isGroupClicked);
  };


  let [showBox, setShowBox] = useState(false);
  let [blackBox, setBlackBox] = useState('');


  let navigate = useNavigate();


  return (
    <Routes>
      <Route path='/more_see' element={<MoreSee />}></Route>
      <Route path='/test' element={<Box />}></Route>
      <Route path='/planet' element={<PlanetList />}></Route>
      <Route path='/galaxy' element={<GalaxyList />}></Route>
      <Route path='/feed_page' element={<FeedPage />}></Route>
      <Route path='/signup' element={<SignUp />}></Route>
      <Route path='/league_detail' element={<LeaguePage />}></Route>
      {/* <Route path='/league_detail' element={<LeagueDetail />}></Route> */}
      <Route path='/notice' element={<Notice />}></Route>
      <Route path='/notice_list' element={<NoticeList />}></Route>
      <Route path='/select_bias' element={<SelectBias />}></Route>
      <Route path='/namecard' element={<NameCard />}></Route>
      <Route path='/mypage' element={<MyPage />}></Route>
      <Route path='/bias_certify' element={<BiasCertify />}></Route>
      <Route path='/bias_info/user_contribution' element={<BiasDetail />}></Route>
      <Route path='/novalogin' element={<NOVALogin />}></Route>
      <Route path='/' element={
        <div onClick={(e) => {
          e.stopPropagation();
          if (showBox) {
            setShowBox(false);
          };
        }} className={`container ${blackBox}`}>

          <div className="top-area">
            <header className='header'>
              <div className='logo' onClick={() => {
                navigate('/');
              }}>
                <img src={logo}></img>
              </div>
              <div className='buttons'>
                <button className='tool-button'>
                  <img src={menu} onClick={() => {
                    navigate('/more_see')
                  }}></img>
                </button>
                {/* <Link to='/' className='button'>홈</Link> */}
                {/* <Link to='/namecard' className='button'>명함</Link> */}
                <Link to='/test' className='button'>테스트</Link>
                {/* <Link to='/planet' className='button'>행성페이지</Link>
                <Link to='/galaxy' className='button'>은하페이지</Link>
                <Link to='/feed_page' className='button'>피드페이지</Link>
                <Link to='/signup' className='button'>회원가입</Link>
                <Link to='/league_detail' className='button'>리그 자세히보기</Link>
                <Link to='/novalogin' className='button'>로그인 페이지</Link> */}
                <Link to='/mypage' className='button'>마이페이지</Link>
                {/* <Link to='/bias_certify' className='button'>최애 지지하기</Link> */}
                {/* <Link to='/league_detail' className='button'>리그상세페이지</Link> */}
                {/* <Link to='/select_bias' className='button'>최애선택</Link> */}
                {/* <Link to='/data_test' className='button'>테스트페이지</Link> */}
                {/* <Link to='/mybias' className='button'>최애페이지</Link> */}
              </div>
            </header>
            <Banner url={url}></Banner>

            <h2 className='authen'>인증하기</h2>

            <section className='my-bias'>
              <MyBias url={url} token={newToken} showBox={showBox} blackBox={blackBox}></MyBias>
            </section>
          </div>

          <section>
            <h2 className='satellite-search'>위성 탐색</h2>
            <InfFeed></InfFeed>
          </section>

          {/* <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">개인리그 랭킹</div>
              <div className={`toggle-container ${isSoloClicked ? "" : "active"}`}>
                <div onClick={() => {
                  handleSoloToggle();

                  // handleTouch('내 최애')
                }} className={`text ${isSoloClicked ? "" : "active"}`}>내 최애</div>
                <div onClick={() => {
                  handleSoloToggle();
                  // handleTouch('전체')
                }} className={`text ${isSoloClicked ? "active" : ""}`}>전체</div>
                <div className="toggle-slider"></div>

              </div>
            </div>
            <Meta url={url} isSoloClicked={isSoloClicked} type={type[0]} token={newToken}></Meta>

          </section>

          <section className="solo-bias-rank">
            <div className='title-area'>
              <div className="ranking">단체리그 랭킹</div>
              <div className={`toggle-container ${isGroupClicked ? "" : "active"}`}>
                <div onClick={() => {
                  handleGroupToggle()
                  // handleTouch('내 최애')
                }} className={`text ${isGroupClicked ? "" : "active"}`}>내 최애</div>
                <div onClick={() => {
                  handleGroupToggle()
                  // handleTouch('전체')
                }} className={`text ${isGroupClicked ? "active" : ""}`}>전체</div>
                <div className="toggle-slider"></div>

              </div>
            </div>
            <Meta url={url} isGroupClicked={isGroupClicked} type={type[1]} token={newToken}></Meta>
          </section> */}

          {/* <section className="advise"></section> */}
          {/* <FloatingButton showSpeaker={showBox} setShowSpeaker={setShowBox}></FloatingButton> */}
          <NavBar></NavBar>
          {/* <footer className="footer">
            <div>
              <p>NOVA</p><br />
              <p className='nova-info'>경북 경산시 압량읍 압독2로1길 21, 1층 184</p>
              <p className='nova-info'>대표: 김민관 | 사업자등록번호: 380-08-03011</p>
              <p className='nova-info'>통신판매업신고번호: 0000-0000-000000</p>
              <p className='nova-info'>전화번호: 010-9875-2508 | 이메일:youths0828@nova-platform.kr</p>
            </div>
            <div className="loundspeaker">
            </div>

          </footer> */}
        </div >


      } />

    </Routes>
  );
}

export default App;