import React from "react";
import Image from "next/image";

export default function Workflow({ title, description, image, onClick }) {
  return (
    <div className="workflow-container" onClick={onClick}>
      <div className="workflow-icon">
        <Image src={image} alt="workflow icon"/>
      </div>
      <div className="workflow-header">
        <div className="font-22-5 color-6" style={{ marginBottom: "0.25rem" }}>
          {title}
        </div>
        <div className="secondary-text">{description}</div>
      </div>
    </div>
  );
}
