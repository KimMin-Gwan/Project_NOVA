import { useEffect, useState } from "react";
import mainApi from "../services/apis/mainApi";

function Banner() {
  let [currentBanner, setBanner] = useState(0);
  let [images, setImage] = useState([]);

  useEffect(() => {
    let copy = [];
    mainApi.get("/home/banner").then((res) => {
      copy = res.data.body.banner.map((banner) => banner.ba_url);
      setImage(copy);
    });
    // fetch(url + "banner")
    //   .then((response) => response.json())
    //   .then((data) => {
    //     copy = data.body.banner.map((banner) => banner.ba_url);
    //     // copy = [data.body.banner[0].ba_url, data.body.banner[1].ba_url];
    //     setImage(copy);
    //   });

    let a = setInterval(() => {
      setBanner((prevIndex) => {
        const nextIndex = (prevIndex + 1) % copy.length;
        return nextIndex;
      });
    }, 3000);

    return () => {
      clearInterval(a);
    };
  }, []);

  return (
    <section className="banner">
      <div className="banner-images">
        {images.map(function (a, i) {
          return (
            <div className="image-box" key={i}>
              <img className="image1" src={images[currentBanner]}></img>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default Banner;
