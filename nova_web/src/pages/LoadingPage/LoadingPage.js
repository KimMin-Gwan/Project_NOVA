///import { RingLoader } from "react-spinners";
///import "./index.css";

///export default function LoadingPage() {
  ///return (
    ///<div className="LoadingPage">
      ///<RingLoader size={100} color="#2863cd" />
    ///</div>
  ///);
///}


import "./index.css";
import loadGIF from "./loading_ani.gif";

export default function LoadingPage() {
  return (
    <div className="LoadingPage">
      <img 
        src={loadGIF} 
        className="BrandLoader" 
      />
    </div>
  );
}