import React from "react";
import "./App.css";
import { Routes, Route } from "react-router-dom"; 

import Signup from "./components/User_Management/Register_User/Register_User.tsx";
import Login from "./components/User_Management/Login_User/Login_User.tsx";
import Home from "./components/Menu_Management/Home/Home.tsx";


const App: React.FC = () => {
  return (
      <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/home" element={<Home />} />
      </Routes>
  );
};

export default App;
