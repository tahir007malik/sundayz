import React from "react";
import { useNavigate } from "react-router-dom";
import "./Notfound.css";

const NotFound = () => {
    const navigate = useNavigate();

    return (
        <div className="not-found-container">
            <h1 className="not-found-title">404</h1>
            <p className="not-found-message">Oops! The page you're looking for doesn't exist.</p>
            <button onClick={() => navigate("/")} className="back-home-btn">
                Landing Page
            </button>
        </div>
    );
};

export default NotFound;
