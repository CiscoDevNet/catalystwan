import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from 'next/navigation'

// const Header = dynamic(() => import("../src/Header"), {
//   ssr: false,
// });

const Home = () => {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    
  }, []);

  return (
    <>
      <div className="m-10 hbr-type">Hello</div>
    </>
  );
};

export default Home;
