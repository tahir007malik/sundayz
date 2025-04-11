import { Routes, Route } from "react-router-dom"; 
import React from "react";
import "./App.css";

import Signup from "./components/User_Management/Register_User/Register_User.tsx";
import Login from "./components/User_Management/Login_User/Login_User.tsx";
import Home from "./components/Menu_Management/Home/Home.tsx";
import Landing from "./components/Landing/Landing.tsx";
import NotFound from "./components/Menu_Management/Notfound/Notfound.tsx";
import ProtectedRoute from "./components/Protected_Route/Protected_Route.tsx";

const App: React.FC = () => {
  return (
      <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route 
              path="/home" 
              element={
                  <ProtectedRoute>
                      <Home />
                  </ProtectedRoute>
              } 
          />
          <Route path="*" element={<NotFound />} />
      </Routes>
  );
};

export default App;
