import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";
import Image from "next/image";
import RightImage from "../public/images/bg-login.svg";

const Home = () => {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {}, []);

  return (
    <div>
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
      <div className="main-container">
        <div className="container-fluid dashboard-main-container mt-2">
          <div className="row">
            <div className="ml-sm-auto mr-sm-auto col-lg-10 mt-4 dashboard-inner-container inner-container">
              <div className="text-center pt-3 h-100">

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
