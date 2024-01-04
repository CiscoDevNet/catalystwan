import React from "react";
import Image from "next/image";
import CiscoLogoWhite from "../public/images/CiscoLogoWhite.svg";

const Header = () => {
  return (
    <section id="header-section">
      <div className="container-fluid pt-5 px-0">
        <div className="container">
          <nav className="navbar navbar-expand-md navbar-light px-0">
            <a className="navbar-brand mr-5 c-pointer">
              <Image priority src={CiscoLogoWhite} alt="Cisco branding" />
            </a>
            <div className="collapse navbar-collapse">
                <ul className="navbar-nav ml-auto">
                    <li className="nav-item"></li>
                    <li className="nav-item c-pointer">
                        <a className="nav-link">About</a>
                    </li>
                </ul>
            </div>
          </nav>
        </div>
      </div>
    </section>
  );
};

export default Header;
