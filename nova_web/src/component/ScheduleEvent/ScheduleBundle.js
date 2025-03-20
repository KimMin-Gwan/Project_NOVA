import style from "./ScheduleEvent.module.css";

export default function BaseBundle({ toggleClick, date, sbname, uname, bname }) {
  return (
    <div className={style["ScheduleEvent"]} onClick={toggleClick}>
      <dl>
        <span className={style["ScheduleBudleTitle"]}>
          <dt>{sbname}</dt>
          <p>{uname} 등록</p>
        </span>
        <dt>{bname}</dt>
        <dt>{date}</dt>
      </dl>
    </div>
  );
}

// 일정탐색 페이지에 일정 번들 컴포넌트
export function ScheduleBundle({ toggleClick, item }) {
  return <BaseBundle toggleClick={toggleClick} {...item} />;
}

//  이벤트 탐색 페이지에 이벤트 추가 컴포넌트
// export function EventBundle({ toggleClick }) {
//   return (
//     <BaseBundle toggleClick={toggleClick}>
//       <div className={style["scheduleBox"]}>
//         <section className={style["BnameInfo"]}>
//           <dt className={style["eventDate"]}>
//             {schedule.date} | {schedule.start}
//           </dt>
//           <dt>{schedule.location}</dt>
//         </section>
//         <section className={style["rightSection"]}>
//           <p>14일 전</p>
//           <p>
//             <b>12</b> 선택
//           </p>
//         </section>
//       </div>
//     </BaseBundle>
//   );
// }
