import dynamic from "next/dynamic";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";
import Workflows from "../src/workflows/Workflows";

const Home = () => {
  const router = useRouter();
  const dispatch = useDispatch();

  return (
    <div className="main-content">
      <div className="heading-div">
        <div className="heading">Select your workflow</div>
      </div>
      <div>
        <Workflows />
      </div>
    </div>
  );
};

export default Home;
