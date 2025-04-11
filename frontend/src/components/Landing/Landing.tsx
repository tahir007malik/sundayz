import React from "react";
import { useNavigate } from "react-router-dom";
import "./Landing.css";

const Landing = () => {
const navigate = useNavigate();

    return (
    <div className="landing-container">
        <h2>Welcome to Sundayz!</h2>
        <p>Your happiness, one scoop at a time!</p>
        <div className="landing-btn-container">
            <button className = "landing-btn-nav" onClick={() => navigate("/login")}>Login</button>
            <button className = "landing-btn-nav" onClick={() => navigate("/signup")}>Sign Up</button>
        </div>
    </div>
    );
};

export default Landing;
