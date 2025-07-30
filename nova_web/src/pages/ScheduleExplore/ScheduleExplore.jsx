import React, { useEffect, useState, useRef } from "react";


import style from "./ScheduleExplore.module.css"

export default function ScheduleExploreDesktop() {

    return(     
        <div className={style["explore_schedule_main_frame"]}>
            <div className={style["explore_schedule_container"]}>
                <div className={style["item_selcet_wrapper"]}>
                    <div className={style["selected_item"]}>게임</div>
                    <div className={style["category_item"]}>저챗</div>
                    <div className={style["category_item"]}>음악</div>
                    <div className={style["category_item"]}>그림</div>
                    <div className={style["category_item"]}>스포츠</div>
                    <div className={style["category_item"]}>시참</div>
                </div>
                
                <div className={style["schedule_grid"]}>
                    <div className={style["schedule_component_wrapper"]}>
                        <div className={style["schedule_wrapper"]}>
                            <span className={style["schedule_title"]}>대충 노래 들으면서 개발하는 방송</span>
                            <div className={style["schedule_detail_container"]}>
                                <span className={style["artist_name"]}>육등성</span>
                                <div className={style["schedule_time_wrapper"]}>
                                    <span className={style["schedule_time"]}>03월 04일 화</span>
                                    <span className={style["schedule_time"]}>오후 06:00</span>
                                </div>
                                <span className={style["schedule_platform"]}>치지직</span>
                            </div>
                        </div>
                        <div className={style["schedule_extra_control_container"]}>
                            <div className={style["schedule_detail"]}>자세히</div>
                            <div className={style["schedule_subscribe"]}>구독하기</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      
    )
  }