import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import fund_img from './../img/funding.png';
import menuBtn_img from './../img/menuBtn.png';
import galaxy_img from './../img/galaxy.png';
import shortForm_img from './../img/short_form.png';

const NavBar = () => {
    const [isVisible, setIsVisible] = useState(false);

    let navigate = useNavigate();

    const toggleNavBar = () => {
        setIsVisible(!isVisible);
    };

    function handleNavigate(path) {
        navigate(path);
    };

    function handleStopClick(e) {
        e.stopPropagation();
    };

    return (
        <div className='nav_button_box'>
            <div className={`nav-box ${isVisible ? 'visible' : ''}`}>
                <button className={`nav_button2`}
                    onClick={(e) => {
                        handleStopClick(e);
                        handleNavigate('/planet');
                    }
                    }>
                    <img src={fund_img} className='btn_img' />
                </button>
                <p>펀딩 페이지</p>
            </div>
            <div className={`nav-box ${isVisible ? 'visible' : ''}`}>
                <button className={`nav_button2`}
                    onClick={(e) => {
                        handleNavigate('/feed_page')
                        handleStopClick(e)
                    }
                    }>
                    <img src={shortForm_img} className='btn_img' />
                </button>
                <p>피드</p>
            </div>
            <div className={`nav-box ${isVisible ? 'visible' : ''}`} >
                <button className={`nav_button3`}
                    onClick={(e) => {
                        handleNavigate('/galaxy');
                        handleStopClick(e);
                    }}>
                    <img src={galaxy_img} className='btn_img' />
                </button>
                <p>은하 리그</p>
            </div>


            <button className='nav_button' onClick={toggleNavBar}>
                <img src={menuBtn_img} className='btn_img' />
            </button>
        </div>
    );
};

export default NavBar;
