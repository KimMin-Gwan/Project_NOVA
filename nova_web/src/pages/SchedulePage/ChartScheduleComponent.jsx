import React, { useState, useRef, useEffect } from 'react';
import './chart_schedule_style.css'

// 보이지않는 300등분을 할것

// 앞 부분에는 padding을 300등분한 길이만큼 줄것

// 본 길이는 실제 길이를 300등분한 길이만큼 줄것
// 끝

export default function ChartScheduleComponent({ timeblocks, sname, bname, color_code, timeSection }) {
    let adjustedWidth = 0; // 앞에 몇 분 임
    let adjustedPadding = 0; // 시작 시간 몇 분임

    // timeSection과 일치하는 timeblock 찾기
    const matchingBlock = timeblocks.find((block) => block.time === timeSection);

    if (matchingBlock) {
        adjustedWidth = matchingBlock.length * 0.2777; // 길이 계산
        adjustedPadding = matchingBlock.start * 0.2777; // 시작 위치 계산
    }

    return (
        <div className="background-box">
            <div
                className="schedule-box"
                style={{
                width: `${adjustedWidth}%`,
                marginLeft: `${adjustedPadding}%`,
                backgroundColor: `${color_code}`,
                }}
            >
                {matchingBlock && matchingBlock.length >= 80 && (
                <>
                    <span>{sname}</span>
                    <span>{bname}</span>
                </>
                )}
            </div>
        </div>

    );
}
