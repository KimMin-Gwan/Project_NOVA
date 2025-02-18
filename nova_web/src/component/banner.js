import { useEffect, useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import mainApi from "../services/apis/mainApi";

import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

// import required modules
import { Autoplay, Pagination } from "swiper/modules";

export default function Banner() {
  const [banners, setBanners] = useState([]);

  function fetchBanner() {
    mainApi.get("/home/banner").then((res) => {
      setBanners(res.data.body.banner);
    });
  }

  useEffect(() => {
    fetchBanner();
  }, []);
  return (
    <Swiper
      centeredSlides={true}
      autoplay={{
        delay: 3000,
        disableOnInteraction: false,
      }}
      pagination={{
        clickable: true,
      }}
      modules={[Autoplay, Pagination]}
      className="mySwiper"
    >
      {banners.map((banner) => (
        <SwiperSlide key={banner.baid}>
          <section className="banner">
            <div className="banner-images">
              <div className="image-box">
                <img src={banner.ba_url} alt={`banner ${banner.baid}`} />{" "}
              </div>
            </div>
          </section>
        </SwiperSlide>
      ))}
    </Swiper>
  );
}
