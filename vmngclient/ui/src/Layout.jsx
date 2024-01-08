import React from "react";
import Image from "next/image";
import RightImage from "../public/images/bg-login.svg";
import Header from "./Header";

export default function Layout({ children }) {
  return (
    <div>
      <Header />
      <div className="side-graphics d-lg-block">
        <Image
          priority
          src={RightImage}
          alt="Right image"
          style={{
            position: "absolute",
            right: "0",
            bottom: "2.2143rem",
            height: "86%",
            width: "7.5rem",
          }}
        />
      </div>
      <div className="main-container mt-4">
        <div className="text-center container-div">
          <main>{children}</main>
        </div>
      </div>
    </div>
  );
}
