import { useState } from 'react';
import style from './ProgressBar.module.css';

function ProgressBar() {

    let [value, setValue] = useState(0);

    function updateValue(point){
        setValue(point);
    };

    return (
        <div className={style['progress-container']}>
            <div className={style['progress-bar']}
            style={{width:`${80}%`}}></div>
        </div>
    )
}

export default ProgressBar;