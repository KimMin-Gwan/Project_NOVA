import { Editor } from "@toast-ui/react-editor";
import colorSyntax from "@toast-ui/editor-plugin-color-syntax";
import "@toast-ui/editor/dist/toastui-editor.css";
import "tui-color-picker/dist/tui-color-picker.css";
import "@toast-ui/editor/dist/i18n/ko-kr";
import "@toast-ui/editor-plugin-color-syntax/dist/toastui-editor-plugin-color-syntax.css";
import { useEffect, useRef } from "react";

export default function EditorBox({ setLongData, editorRef, initialValue }) {
  const onChange = () => {
    setLongData(editorRef.current.getInstance().getHTML());
  };

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.getInstance().setHTML(initialValue);
    }
  }, [editorRef, initialValue]);

  return (
    <Editor
      ref={editorRef}
      initialValue={initialValue}
      placeholder="내용을 입력해주세요"
      height="100%"
      initialEditType="wysiwyg"
      useCommandShortcut={false}
      plugins={[colorSyntax]}
      hideModeSwitch={true}
      onChange={onChange}
      language="ko-KR"
      toolbarItems={[["bold", "italic", "strike"]]}
    />
  );
}
