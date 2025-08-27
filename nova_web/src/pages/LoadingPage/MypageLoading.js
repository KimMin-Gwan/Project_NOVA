//import { BeatLoader } from "react-spinners";
//<BeatLoader size={20} color="#2863cd" />

import "./index.css";
import loading_ani2 from "./loading_ani2.gif";


export default function MyPageLoading() {
  return (
    <div className="MyPageLoading">
      <img src={loading_ani2}
        className="DefaultLoader"
      />
    </div>
  );
}
