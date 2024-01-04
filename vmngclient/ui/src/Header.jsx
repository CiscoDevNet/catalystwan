import React from "react";
import reactWrapper from "@harbor/elements/utils/react/wrapper";
import Image from "next/image";

const [HbrHeader, HbrIcon] = reactWrapper(["hbr-shell-header", "hbr-icon"]);

const Brand = (
    <a href="" slot="logo-name" style={{marginLeft: "4px"}}>
      <HbrIcon name="cisco"></HbrIcon>
      <div>Vmanage Client</div>
    </a>
  );

const Header = () => {
  return (
    <HbrHeader
      className="sticky top-0 flex flex-wrap"
      style={{
        zIndex: "var(--hbr-z-index-shell)",
        background: "linear-gradient(119deg,#54b1e5,#165d97)",
      }}
    >
      {Brand}
    </HbrHeader>
  );
};

export default Header;
