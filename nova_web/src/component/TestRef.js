import { useEffect } from "react";
import { useRef } from "react";

export default function TestRef() {
  let commentRef = useRef();

  useEffect(() => {
    commentRef.current.focus();
  }, []);
  return (
    <div>
      <input ref={commentRef} type="text" />
    </div>
  );
}
