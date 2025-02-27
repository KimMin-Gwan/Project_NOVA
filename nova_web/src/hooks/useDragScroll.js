import { useRef, useState } from "react";

export default function useDragScroll() {
  let scrollRef = useRef(null);
  let [isDrag, setIsDrag] = useState(false);
  let [dragStart, setDragStart] = useState("");
  let [hasDragged, setHasDragged] = useState(false);

  function onMouseDown(e) {
    e.preventDefault();
    setIsDrag(true);
    setDragStart(e.pageX + scrollRef.current.scrollLeft);
    setHasDragged(false);
  }

  function onMouseUp(e) {
    if (hasDragged) {
      e.stopPropagation();
      e.preventDefault();
    }
    setIsDrag(false);
  }

  function onMouseMove(e) {
    if (isDrag) {
      scrollRef.current.scrollLeft = dragStart - e.pageX;
      setHasDragged(true);
    }
  }

  return {
    scrollRef,
    hasDragged,
    dragHandlers: {
      onMouseDown,
      onMouseMove,
      onMouseUp,
    },
  };
}
