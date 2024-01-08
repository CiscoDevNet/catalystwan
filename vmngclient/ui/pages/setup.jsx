import React from "react";
import VmanageSetup from "../src/workflows/VmanageSetup.jsx";

export default function Setup() {
  return (
    <div className="main-content">
      <div className="mb-2 heading-div">
        <div className="heading">Enter details for source vManage</div>
      </div>
        <VmanageSetup />
    </div>
  );
}
