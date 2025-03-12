import "./CategoryModal/index.css";
import ModalRectangle from "./../img/ModalRectangle.png";
import ScheduleSelect from "./ScheduleSelect/ScheduleSelect";

export default function TestRef() {
  return (
    <div className={`CategoryModal see`}>
      <div className={`modal-container on`} onClick={(e) => e.stopPropagation()}>
        <section className="top-section">
          <img src={ModalRectangle} alt="모달 사각형" />
          <div className="modal-title">주제 이름</div>
        </section>
        <ScheduleSelect />
      </div>
    </div>
  );
}
