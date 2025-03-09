import React from 'react';

import './event_style.css'; // Corrected import for CSS file

const EventComponent = () => {
    return (
        <div className='event-container'>
            <span className='event-name'>하이블루밍 데뷔</span>
            <span className='bias-name'>OVERTHEWALL</span>
            <span className='bias-name'>치지직, 오후 3:00</span>
        </div>
    );
};

export default EventComponent;