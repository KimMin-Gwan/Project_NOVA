import { BeatLoader } from "react-spinners";
import "./index.css";

export default function MyPageLoading() {
  return (
    <div className="MyPageLoading">
      <BeatLoader size={20} color="#2863cd" />
    </div>
  );
}
