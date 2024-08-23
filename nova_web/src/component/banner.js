import { useEffect, useState } from 'react';
import axios from 'axios';

function Banner({ url }) {
  let [currentBanner, setBanner] = useState(0);
  let [images, setImage] = useState([]);
  // 
  // let url = 'http://nova-platform.kr/home/banner';
  // let data = { token: '토큰 정보'}

  useEffect(() => {
    let copy = [];
    fetch(url + 'banner')
      .then(response => response.json())
      .then(data => {
        // console.log(data)
        copy = data.body.banner.map(banner => banner.ba_url);
        // copy = [data.body.banner[0].ba_url, data.body.banner[1].ba_url];
        setImage(copy);
      });

    let a = setInterval(() => {
      setBanner((prevIndex) => {
        const nextIndex = (prevIndex + 1) % copy.length;
        return nextIndex;
      })
    }, 3000)
    //   copy.map(function(b, i){
    //   if(copy.length>i)
    //   {
    //     setImage([copy[0]]);
    //   }
    // })

    return () => {
      clearInterval(a);
      // setImage([copy[0]]);
    };
  }, [url])

  return (
    <section className="banner">
      <div className="banner-images">
        {
          images.map(function (a, i) {
            return (
              <div className="image-box" key={i}>
                <img className="image1" src={images[currentBanner]}></img>
              </div>
            )
          })
        }

        {/* <div className="image-box">
          <img className="image1" src={images[currentBanner]}></img>
        </div> */}
        {/* <div className="image-box">
          <img className="image2" src={url}></img>
        </div> */}
      </div>
    </section>
  )
}

export default Banner;


