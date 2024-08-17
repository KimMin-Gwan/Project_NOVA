import img1 from '../img/img1.jpg';
import img2 from '../img/img2.jpg';
import img3 from '../img/img3.jpeg';
import { useEffect, useState } from 'react';
import axios from 'axios';

function Banner() {
  let [currentBanner, setBanner] = useState(1);
  let [images, setImage] = useState([]);
  // 
  let url = 'http://127.0.0.1:80/home/banner';
  // let data = { token: '토큰 정보'}
  // useEffect(() => {
  //   // let a = setTimeout(()=>{ setBanner(currentBanner=1)}, 2000)
  //   return () => {
  //     // clearTimeout(a);
  //     // setBanner(currentBanner=0);
  //   }
  // // }, [])
  // function getImages(){
  //   return ()
  // }

  useEffect(() => {
    fetch(url)
      .then(response => response.json())
      .then(data => {
        let copy = [...data.body.banner];
        setImage(copy[0].ba_url);
        // console.log(copy);
        // console.log(JSON.stringify(copy[0].ba_url));
        // setImage(copy[1].ba_url);
        // console.log(JSON.stringify(images));
        // console.log(images)
      });
    // let a = setTimeout(()=>{ setImage(0)},2000)

    return () => {
      // clearTimeout(a);
    }
  }, [])

  return (
    <section className="banner">
      <div className="banner-images">
        {/* {
          images.map(function (a, i) {
            return (
              <div className="image-box" key={i}>
                <div>{images}</div>
                <img className="image1" src={images}></img>
              </div>
            )
          })
        } */}

        <div className="image-box">
          <img className="image1" src={images}></img>
        </div>
        {/* <div className="image-box">
          <img className="image2" src={url}></img>
        </div> */}
      </div>
      <div className="banner-indicator">2/5</div>

    </section>
  )
}

export default Banner;


