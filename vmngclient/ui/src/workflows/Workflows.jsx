import React from "react";
import { useRouter } from "next/navigation";
import Workflow from "./Workflow";

import SetupVmanage from "../../public/images/SetupVmanage.svg";
import Convert from "../../public/images/Convert.svg";

export default function Workflows() {
  const { push } = useRouter();
  return (
    <div className="workflows-container">
      <Workflow
        title="Setup vManage"
        description="Setup vManage"
        image={SetupVmanage}
        onClick={() => push("/setup")}
      />
      <Workflow
        title="Convert"
        description="Convert"
        image={Convert}
        onClick={() => push("/convert")}
      />
    </div>
  );
}
