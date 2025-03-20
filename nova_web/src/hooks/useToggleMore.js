import { useState } from "react";

const useToggleMore = () => {
  const [moreClick, setMoreClick] = useState({});

  // 버튼 나오게 하는 함수
  const handleToggleMore = (id) => {
    setMoreClick((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  return { moreClick, handleToggleMore };
};

export default useToggleMore;
