import { Editor } from "@toast-ui/react-editor";
import colorSyntax from "@toast-ui/editor-plugin-color-syntax";
import "@toast-ui/editor/dist/toastui-editor.css";
import "tui-color-picker/dist/tui-color-picker.css";
import "@toast-ui/editor/dist/i18n/ko-kr";
import "@toast-ui/editor-plugin-color-syntax/dist/toastui-editor-plugin-color-syntax.css";
import { useRef } from "react";

export default function EditorBox({ setLongData, editorRef, initialValue }) {

  const onChange = () => {
    const data = editorRef.current.getInstance().getHTML();
    setLongData(data);
  };

  editorRef.current?.getInstance().setHTML(initialValue);

  return (
      <Editor
        ref={editorRef}
        initialValue={initialValue}
        placeholder="내용을 입력해주세요"
        // previewStyle="vertical"
        height="100%"
        initialEditType="wysiwyg"
        useCommandShortcut={false}
        plugins={[colorSyntax]}
        hideModeSwitch={true}
        onChange={onChange}
        language="ko-KR"
        toolbarItems={[
          ["heading", "bold", "italic", "strike"] // headings - 1,2,3
        ]}
      />
  );
}
