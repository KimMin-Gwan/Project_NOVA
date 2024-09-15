import React, { useState } from 'react';

const NavBar = () => {
    const [isVisible, setIsVisible] = useState(false);

    const toggleNavBar = () => {
        setIsVisible(!isVisible);
    };

    return (
        <div className='nav_button_box'>
            <button className={`nav_button2 ${isVisible ? 'visible' : ''}`}>click2</button>
            <button className={`nav_button3 ${isVisible ? 'visible' : ''}`}>click3</button>
            <button className='nav_button' onClick={toggleNavBar}>click</button>
        </div>
    );
};

export default NavBar;
