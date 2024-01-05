import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";
import Workflows from "../src/workflows/Workflows";

const Home = () => {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {}, []);

  return (
    <div>
      <div className="main-container">
        <div className="text-center mt-4 container-div">
          <div className="main-content">
            <div className="heading-div">
              <div className="heading">Select your workflow</div>
            </div>
            <div>
              <Workflows/>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
