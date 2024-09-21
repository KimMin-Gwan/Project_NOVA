import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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
                        handleNavigate('/planet')
                        handleStopClick(e)
                    }
                    }>펀딩</button>
                <p>펀딩 페이지</p>
            </div>
            <div className={`nav-box ${isVisible ? 'visible' : ''}`}>
                <button className={`nav_button2`}
                    onClick={(e) => {
                        handleNavigate('/planet')
                        handleStopClick(e)
                    }
                    }>행성</button>
                <p>행성 탐색</p>
            </div>
            <div className={`nav-box ${isVisible ? 'visible' : ''}`}>
                <button className={`nav_button3`}
                    onClick={(e) => {
                        handleNavigate('/galaxy');
                        handleStopClick(e);
                    }}>은하</button>
                <p>행성 탐색</p>
            </div>


            <button className='nav_button' onClick={toggleNavBar}>click</button>
        </div>
    );
};

export default NavBar;
