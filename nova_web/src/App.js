import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="container">
      <header className='header'>
        <div className='logo'>로고</div>
        <div className='buttons'>
          <button>돌아가기</button>
          <button>마이페이지</button>
        </div>
      </header>

      <section className="banner">
        <div>베너</div>
        <div className="banner-indicator">1/5</div>
      </section>

      <section className="authentication">
        <div className="authentication-title">인증하기</div>
        <div className="item-box">
          <div className="profile">
            <div>이미지</div>
          </div>
          <div className="name">이름</div>
          <button className="auth-button">인증하기</button>
        </div>
        <div className="item-box">
          <div className="profile">
            <div>플러스</div>
          </div>
          <div className="name">최애 지지하기 (그룹)</div>
        </div>
      </section>

      <section>
        <div className="ranking">최애의 랭킹</div>
        <div className="ranking-tabs">
          <div className='tab'>최애의 리그</div>
          <div className='tab'>전체 리그</div>
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

      <footer className="footer">
        <p>사업명 및 다양한 정보를 etc...</p>
        <button className="confirm-button">확성기</button>
      </footer>
    </div>
  );
}

export default App;