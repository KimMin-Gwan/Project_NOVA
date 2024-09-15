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
            <button className={`nav_button2 ${isVisible ? 'visible' : ''}`}
                onClick={(e) => {
                    handleNavigate('/planet')
                    handleStopClick(e)
                }
                }>행성</button>
            <button className={`nav_button3 ${isVisible ? 'visible' : ''}`}
                onClick={(e) => {
                    handleNavigate('/galaxy');
                    handleStopClick(e);
                }}>은하</button>
            <button className='nav_button' onClick={toggleNavBar}>click</button>
        </div>
    );
};

export default NavBar;
