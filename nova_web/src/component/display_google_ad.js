import React, { useEffect } from 'react'

const DisplayAds = () => {
  useEffect(() => {
    const pushAd = () => {
      try {
        const adsbygoogle = window.adsbygoogle
        // //console.log({ adsbygoogle })
        adsbygoogle.push({})
      } catch (e) {
        console.error(e)
      }
    }

    let interval = setInterval(() => {
      // Check if Adsense script is loaded every 300ms
      if (window.adsbygoogle) {
        pushAd()
        // clear the interval once the ad is pushed so that function isn't called indefinitely
        clearInterval(interval)
      }
    }, 300)

    return () => {
      clearInterval(interval)
    }
  }, [])
  return (
    <ins
      className='adsbygoogle'
      style={{ display: 'inline-block;width:300px;height:90px' }}
      data-ad-client='ca-pub-6082753133500429'
      data-ad-slot='1007662628'
      //data-ad-format='auto'
      //data-full-width-responsive='true'
    ></ins>
  )
}

export default DisplayAds