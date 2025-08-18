import React from 'react';

import './event_style.css'; // Corrected import for CSS file

export default function EventComponent({
  sename,
  bname,
  platform,
  date
}) {
    return (
        <div className='event-container'>
            <span className='event-name'>{sename}</span>
            <span className='bias-name'>{bname}</span>
            <span className='bias-name'>{platform}, {date}</span>
        </div>
    );
};
