import { useState } from 'react';
import style from './ProgressBar.module.css';

function ProgressBar({ point }) {

    let [value, setValue] = useState(0);

    function updateValue(point) {
        setValue(point);
    };

    return (
        <div className={style['progress-container']}>
            <div className={style['progress-bar']}
                style={{ width: `${point}%` }}></div>
        </div>
    )
}

export default ProgressBar;