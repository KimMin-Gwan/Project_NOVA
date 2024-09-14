import React, { useState } from 'react';

const NavBar = () => {
    const [isVisible, setIsVisible] = useState(false);

    const toggleNavBar = () => {
        setIsVisible(!isVisible);
    };

    return (
        <>
            <button className='nav_button' onClick={toggleNavBar}>click</button>
            {
                isVisible && (
                    <>
                        <button className={`nav_button2 ${isVisible ? 'visible' : ''}`}>click2</button>
                        <button className={`nav_button3 ${isVisible ? 'visible' : ''}`}>click3</button>
                    </>
                )
            }
        </>
    );
};

export default NavBar;
