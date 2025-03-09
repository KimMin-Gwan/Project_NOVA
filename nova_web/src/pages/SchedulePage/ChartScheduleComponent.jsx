import React, { useState, useRef, useEffect } from 'react';
import './chart_schedule_style.css'

// 보이지않는 300등분을 할것

// 앞 부분에는 padding을 300등분한 길이만큼 줄것

// 본 길이는 실제 길이를 300등분한 길이만큼 줄것
// 끝

export default function ChartScheduleComponent({schedule_detail, bias_name, start, length, color_code}) {
    const adjustedWidth = length * 0.2777;  // 앞에 몇 분 임
    const adjsutedPadding = start * 0.2777;  //  시작 시간 몇 분임

    return (
        <div className='background-box'>
            <div
             className='schedule-box'
             style={{ 
                width: `${adjustedWidth}%`,
                marginLeft: `${adjsutedPadding}%`,
                backgroundColor: `${color_code}`
             }}
            >
                <span>{schedule_detail}</span>
                <span>{bias_name}</span>
            </div>
        </div>
    );
};
