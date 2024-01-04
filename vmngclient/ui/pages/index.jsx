import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from 'next/navigation'

const Header = dynamic(() => import("../src/Header"), {
  ssr: false,
});

const Home = () => {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    
  }, []);

  return (
    <>
      <Header id="header"/>
      <div className="row">Hello</div>
    </>
  );
};

export default Home;
