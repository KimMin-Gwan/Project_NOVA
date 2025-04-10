import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Swiper, SwiperSlide } from "swiper/react";

import './paymentpage.css';

export default function PaymentPage(){
  const [amount, setAmount] = useState(0);
  const [points, setPoints] = useState(0);

  const addAmount = (value) => {
    const newAmount = amount + value;
    setAmount(newAmount);
    setPoints(Math.floor(newAmount / 2));
  };

  return (
     <div className="charging-page-container">
      <div className="charging-page-box">
        <div className="header">
          <button className="back-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="icon"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>
          <h1 className="title">충전하기</h1>
          <div></div>
        </div>
        <div className="section">
          <h2 className="section-title">충전 금액</h2>
          <div className="input-group">
            <input
              id="amount"
              type="text"
              className="amount-input"
              placeholder="0"
              value={amount}
              readOnly
            />
            <span className="currency">원</span>
          </div>
          <div className="button-group">
            <button
              onClick={() => addAmount(1000)}
              className="add-button"
            >
              + 1,000
            </button>
            <button
              onClick={() => addAmount(10000)}
              className="add-button"
            >
              + 10,000
            </button>
            <button
              onClick={() => addAmount(50000)}
              className="add-button"
            >
              + 50,000
            </button>
          </div>
          <p className="note">1,000원 단위로 결제 가능합니다.</p>
        </div>
        <div className="section">
          <h2 className="section-title">획득 포인트</h2>
          <div className="input-group">
            <input
              id="points"
              type="text"
              className="points-input"
              placeholder="0"
              value={points}
              readOnly
            />
            <span className="currency">PT</span>
          </div>
          <p className="note">충전 금액 2원당 1 PT로 변경해서 표시되게 할 것</p>
        </div>
        <div className="section">
          <h2 className="section-title">결제 수단</h2>
          <div className="payment-method">
            <span>N pay</span>
            <button className="select-button"></button>
          </div>
          <button className="add-payment-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="icon"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            결제 수단 추가
          </button>
        </div>
        <div className="footer-note">
          <p>*결제 금액에는 세금이 포함되어 있습니다.</p>
          <p>*만 19세 미만 미성년자 회원은 법정대리인의 동의가 필요하며, 동의가 완료된 후 포인트 충전 서비스 이용이 가능합니다.</p>
        </div>
        <button className="charge-button">충전하기</button>
      </div>
    </div>
  );
};

