import React from 'react';
import './time_week_style.css'

export default function TimeWeekComponent({date, day, num_schedule}) {
    const adjustedHeight = 74 * num_schedule;

    return (
        <div
         className='time-week-box'
            style={{ 
                height: `${adjustedHeight}px`}}
         >
            <span>{date}</span>
            <span>{day}</span>
        </div>
    );
};
