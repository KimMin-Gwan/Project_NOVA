import React, { useState } from 'react';

import Feed, { InputFeed, InfoArea, Text, Comments } from './feed';

import style from './../pages/FeedPage/FeedPage.module.css';
import stylePlanet from './../pages/PlanetPage/Planet.module.css';
import planet2 from './../img/planet2.png';

import './DraggableBox.css'; // CSS 파일을 연결
import { useNavigate } from 'react-router-dom';

const Box = () => {

  let navigate = useNavigate();


  return (
    <div className={style['test_container']}>
      <div className={`${stylePlanet['top_area']} ${style['top_bar_area']}`}>
        <div onClick={() => { navigate(-1) }}>뒤로</div>
        <div>은하계 탐색</div>
      </div>

      <div className={style.test}>
        <div className={style['short_form_container']}>
          <div className={style['short_box']}>
            <div className={style['img_circle']}></div>
            <div style={{ height: '80px' }}></div>
            <div className={style['short_feed']}>
              <div>
                <InfoArea color={'#7960EC'} name={`행성`} supporter='ㅇㅇㅇ'></InfoArea>
                <Text title='하이' data='ㅇㄴㅁ'></Text>
                <div className={`${style['button_container']} `}>
                  <button className={`${style['select_button']} `}>갑니다</button>
                  <button className={`${style['select_button']} `}>패스</button>
                </div>
              </div>

              <div style={{ width: '100%', height: '10px' }}></div>
              <div className={style.line}></div>
              <Comments></Comments>
            </div>
          </div>

          <div className={style['function_button']}>
            <div className={style['func_btn']}>
              <button></button>
              <p>1.6k</p>
            </div>
            <div className={style['func_btn']}>
              <button></button>
              <p>42</p>
            </div>
            <div className={style['func_btn']}>
              <button></button>
              <p>공유</p>
            </div>
            <div className={style['func_btn']}>
              <button></button>
              <p>신고</p>
            </div>
          </div>
        </div>
      </div>

      <div className={style['short_form_container']}>
        <div className={style['short_box']}>
          <div className={style['img_circle']}></div>
          <div style={{ height: '80px' }}></div>
          <div className={style['short_feed']}>
            <div>
              <InfoArea color={'#7960EC'} name={`행성`} supporter='ㅇㅇㅇ'></InfoArea>
              <Text title='하이' data='ㅇㄴㅁ'></Text>
              <div className={`${style['button_container']} `}>
                <button className={`${style['select_button']} `}>갑니다</button>
                <button className={`${style['select_button']} `}>패스</button>
              </div>
            </div>

            <div style={{ width: '100%', height: '10px' }}></div>
            <div className={style.line}></div>
            <Comments></Comments>
          </div>
        </div>

        <div className={style['function_button']}>
          <div className={style['func_btn']}>
            <button></button>
            <p>1.6k</p>
          </div>
          <div className={style['func_btn']}>
            <button></button>
            <p>42</p>
          </div>
          <div className={style['func_btn']}>
            <button></button>
            <p>공유</p>
          </div>
          <div className={style['func_btn']}>
            <button></button>
            <p>신고</p>
          </div>
        </div>
      </div>
    </div>


  );
};

export default Box;
