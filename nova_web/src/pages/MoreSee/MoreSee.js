import style from './MoreSee.module.css';
import backword from './../../img/back.png';
import vector from './../../img/Vector.png';
import x_icon from './../../img/x_icon.png';
import discord_icon from './../../img/discord_icon.png';
import insta_icon from './../../img/insta_icon.png';
import youtube_icon from './../../img/youtube_icon.png';
import { useNavigate } from 'react-router-dom';

function MoreSee() {

    let navigate = useNavigate();
    let tokenCheck = localStorage.getItem('jwtToken');

    return (
        <div className={style.font}>
            <div class={style.container}>
                <div class={style.TopBar}>
                    <img src={backword} alt="Arrow" class={style.backword} onClick={() => {
                        navigate(-1)
                    }} />
                    <div class={style.TitleBox}>
                        <p class={style.titleName}> 더보기 </p>
                    </div>
                </div>
                <div class={style.content}>
                    <div class={style.mainComponent} onClick={() => {
                        if (tokenCheck) {
                            navigate('/mypage');
                        }
                        else {
                            navigate('/novalogin');
                        }
                    }}>
                        <p class={style.bodyText}>{tokenCheck ? '마이페이지' : '로그인'}</p>
                        <img src={vector} alt="Arrow" class={style.vector} />
                    </div>
                    <div class={style.mainComponent}>
                        <p class={style.bodyText}>최애 신청하기(네이버 폼)</p>
                        <img src={vector} alt="Arrow" class={style.vector} />
                    </div>
                    <div class={style.mainComponent} onClick={() => {
                        navigate('/notice_list')
                    }}>
                        <p class={style.bodyText}>공지사항</p>
                        <img src={vector} alt="Arrow" class={style.vector} />
                    </div>
                    <div class={style.mainComponent}>
                        <p class={style.bodyText}>사업자 정보 및 사용약관</p>
                        <img src={vector} alt="Arrow" class={style.vector} />
                    </div>
                </div>
                <div class={style.inquiry}>
                    <div class={style.iconBox}>
                        <img src={x_icon} alt="Icon" class={style.icon_img} />
                        <p class={style.icon_name}> X </p>
                    </div>
                    <div class={style.iconBox}>
                        <img src={discord_icon} alt="Icon" class={style.icon_img} />
                        <p class={style.icon_name}> Discord </p>
                    </div>
                    <div class={style.iconBox}>
                        <img src={insta_icon} alt="Icon" class={style.icon_img} />
                        <p class={style.icon_name}> Instagram </p>
                    </div>
                    <div class={style.iconBox}>
                        <img src={youtube_icon} alt="Icon" class={style.icon_img} />
                        <p class={style.icon_name}> Youtube </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MoreSee;