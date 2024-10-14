import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import fund_img from './../img/funding.png';
import menuBtn_img from './../img/menuBtn.png';
import galaxy_img from './../img/galaxy3.png';
import shortForm_img from './../img/short_form2.png';
import new_feed from './../img/new_feed2.png';

const NavBar = ({isUserState}) => {
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
        <div className='bottom_bar'>
            <div className='nav_button_box'>
                <button className='nav_button' onClick={() => window.location.reload()}>
                    <img src={galaxy_img} className='btn_img' />
                     <p className='btn_text'>홈</p>
                </button>
            </div>
            <div className='nav_button_box'>
                <button className='nav_button'>
                    <img src={new_feed} className='btn_img' />
                    <p className='btn_text'>만들기</p>
                </button>
            </div>
            <div className='nav_button_box'>
                <button className='nav_button' onClick={(e) => {
                    handleNavigate('/feed_page')
                    handleStopClick(e)
                }}>
                <img src={shortForm_img} className='btn_img' />
                <p className='btn_text'>쇼트폼</p>
                </button>
            </div>
        </div>
    );
};

export default NavBar;
