import style from './MoreSee.module.css';
import backword from './../../img/back.png';
import vector from './../../img/Vector.png';
import x_icon from './../../img/x_icon.png';
import discord_icon from './../../img/discord_icon.png';
import insta_icon from './../../img/insta_icon.png';
import youtube_icon from './../../img/youtube_icon.png';
import { useNavigate } from 'react-router-dom';

function MoreSee() {

    const requestURL = 'https://naver.me/xGImCJSN';

    function handleRequestURL() {
        window.open(requestURL, '_blank', "noopener, noreferrer");
    };

    let navigate = useNavigate();
    let tokenCheck = localStorage.getItem('jwtToken');

    return (
        <div className={style.font}>
            <div className={style.container}>
                <div className={style.TopBar}>
                    <img src={backword} alt="Arrow" className={style.backword} onClick={() => {
                        navigate(-1)
                    }} />
                    <div className={style.TitleBox}>
                        <p className={style.titleName}> 더보기 </p>
                    </div>
                </div>
                
                <div className={style.content}>
                    <div className={style.mainComponent} onClick={() => {
                        if (tokenCheck) {
                            navigate('/mypage');
                        }
                        else {
                            navigate('/novalogin');
                        }
                    }}>
                        <p className={style.bodyText}>{tokenCheck ? '마이페이지' : '로그인'}</p>
                        <img src={vector} alt="Arrow" className={style.vector} />
                    </div>
                    <div className={style.mainComponent} onClick={handleRequestURL}>
                        <p className={style.bodyText}>최애 신청하기(네이버 폼)</p>
                        <img src={vector} alt="Arrow" className={style.vector} />
                    </div>
                    <div className={style.mainComponent} onClick={() => {
                        navigate('/notice_list')
                    }}>
                        <p className={style.bodyText}>공지사항</p>
                        <img src={vector} alt="Arrow" className={style.vector} />
                    </div>
                    <div className={style.mainComponent}>
                        <p className={style.bodyText}>사업자 정보 및 사용약관</p>
                        <img src={vector} alt="Arrow" className={style.vector} />
                    </div>
                    <div className={style.mainComponent}>
                        <p className={style.bodyText}>페이지 설정</p>
                        <img src={vector} alt="Arrow" className={style.vector} />
                    </div>
                </div>

                <div className={style.inquiry}>
                    <div className={style.iconBox}>
                        <img src={x_icon} alt="Icon" className={style.icon_img} />
                        <p className={style.icon_name}> X </p>
                    </div>
                    <div className={style.iconBox}>
                        <img src={discord_icon} alt="Icon" className={style.icon_img} />
                        <p className={style.icon_name}> Discord </p>
                    </div>
                    <div className={style.iconBox}>
                        <img src={insta_icon} alt="Icon" className={style.icon_img} />
                        <p className={style.icon_name}> Instagram </p>
                    </div>
                    <div className={style.iconBox}>
                        <img src={youtube_icon} alt="Icon" className={style.icon_img} />
                        <p className={style.icon_name}> Youtube </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MoreSee;