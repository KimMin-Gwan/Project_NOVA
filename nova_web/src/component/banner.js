import img1 from '../img/img1.jpg';
import img2 from '../img/img2.jpg';
import img3 from '../img/img3.jpeg';
import { useEffect, useState } from 'react';
import axios from 'axios';

// axios.defaults.withCredentials = true;

function Banner() {
  let images = [img1, img2, img3];
  let [currentBanner, setBanner] = useState(1);
  let [image, setImage] = useState('');
  // 
  let url = '/home/banner';
  // let data = { token: '토큰 정보'}
  // useEffect(() => {
  //   // let a = setTimeout(()=>{ setBanner(currentBanner=1)}, 2000)
  //   return () => {
  //     // clearTimeout(a);
  //     // setBanner(currentBanner=0);
  //   }
  // }, [])

  return (
    <section className="banner">
      <div className="banner-images">
        <div className="image-box">
          <img className="image1" src={image}></img>
        </div>
        <div className="image-box">
          <img className="image2" src={url}></img>
        </div>
      </div>
      <div className="banner-indicator">2/5</div>
    </section>
  )
}

export default Banner;