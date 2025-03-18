import style from "./../../pages/Write/WriteFeed.module.css";

export default function Button({ type, children, onClick, disabled }) {
  const getButtonType = () => {
    switch (type) {
      case "close":
        return style["close_button"];
      case "apply":
        return `${style["apply_button"]} ${disabled ? "" : style["apply_button_on"]}`;
      default:
        return style["default_button"];
    }
  };

  return (
    <button className={getButtonType()} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
