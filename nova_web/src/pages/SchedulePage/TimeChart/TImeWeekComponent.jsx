import React from 'react';
import './time_week_style.css'

export default function TimeWeekComponent({date, day, num_schedule, is_today}) {
    console.log(is_today)
    const adjustedHeight = 72 * num_schedule + (num_schedule-1) * 2;
    return (
        <div
         className='time-week-box'
            style={{ 
                height: `${adjustedHeight}px`,
                backgroundColor: is_today ? '#8EBFFF' : '#d0e4ff'
            }}
         >
            <span>{date}</span>
            <span>{day}</span>
        </div>
    );
};
