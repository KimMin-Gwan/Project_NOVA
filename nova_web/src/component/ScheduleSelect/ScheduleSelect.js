import { useState } from "react";
import Input from "../Input/Input";
import "./index.css";

export default function ScheduleSelect() {
  return (
    <div className="ScheduleSelect">
      <Input type={"text"} placeholder={"일정 상세"} />
      <Input placeholder={"장소"} />
    </div>
  );
}
