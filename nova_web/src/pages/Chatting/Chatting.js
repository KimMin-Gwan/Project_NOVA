import style from './Chatting.module.css';

export default function Chatting() {

    return (
        <div className={style["chat-room"]}>
            <div className={style.messages}>
                <div className={style.message}>1</div>

            </div>
            <div className={style["input-box"]}>
                <input
                    type="text"
                />
                <button>Send</button>
            </div>
        </div>
    );
}