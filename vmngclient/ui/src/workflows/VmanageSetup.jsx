import React from "react";
import { useEffect, useState } from "react";

export default function VmanageSetup() {
  const [ip, setIp] = useState("");
  const [port, setPort] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const onPortChange = (e) => {
    const re = /^[0-9\b]+$/;
    if (e.target.value === "" || re.test(e.target.value)) {
      setPort(e.target.value);
    }
  };

  const onSubmit = (e) => {
    e.preventDefault();
  }

  return (
    <form action="post" className="base-form">
      <div className="base-form-entry">
        <span className="form-label">Name</span>
        <div className="form-group">
          <input
            type="text"
            className="form-control"
            onChange={(e) => setName(e.target.value)}
            value={name}
            placeholder="Custom name for saved vmange credentials"
          />
        </div>
      </div>
      <div className="base-form-entry">
        <span className="form-label">vManage IP</span>
        <div className="form-group">
          <input type="text" className="form-control" />
        </div>
      </div>
      <div className="base-form-entry">
        <span className="form-label">vManage Port</span>
        <div className="form-group">
          <input
            type="text"
            className="form-control"
            onChange={(e) => onPortChange(e)}
            value={port}
          />
        </div>
      </div>
      <div className="base-form-entry">
        <span className="form-label">Username</span>
        <div className="form-group">
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
      </div>
      <div className="base-form-entry">
        <span className="form-label">Password</span>
        <div className="form-group">
          <input
            type="text"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>
      <button type="button" className="form-btn" onSubmit={e => onSubmit(e)}>Save</button>
    </form>
  );
}
