import { useState } from "react";

const useToggleMore = () => {
  const [moreClick, setMoreClick] = useState({});

  // 버튼 나오게 하는 함수
  const toggleMore = (id) => {
    setMoreClick((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  return { moreClick, toggleMore };
};

export default useToggleMore;
