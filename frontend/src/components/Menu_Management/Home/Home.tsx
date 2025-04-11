import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const Home = () => {
    const [message, setMessage] = useState("Loading...");
    const [status, setStatus] = useState(""); // Track status ('success' or 'error')
    const [toastMessage, setToastMessage] = useState<string | null>(null); // State for toast message
    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://localhost:8000/", {
            method: "GET",
            credentials: "include", // Include session credentials
        })
            .then((response) => response.json())
            .then((data) => {
                setMessage(data.message); // Set the message directly from backend
                setStatus(data.status); // Track status for conditional styling
            })
            .catch(() => {
                setMessage("An unexpected error occurred.");
                setStatus("error");
            });
    }, []);

    const handleLogout = async () => {
        try {
            const response = await fetch("http://localhost:8000/logout", {
                method: "POST",
                credentials: "include", // Ensure session cookies are included
            });

            const data = await response.json();

            if (response.ok) {
                setToastMessage(data.message); // Show success toast
                setTimeout(() => {
                    setToastMessage(null); // Hide toast after 3 seconds
                    navigate("/login"); // Redirect to login page
                }, 3000);
            } else {
                setToastMessage(data.message || "Failed to log out."); // Show error toast
                setTimeout(() => setToastMessage(null), 3000); // Hide toast after 3 seconds
            }
        } catch (error) {
            console.error("Error during logout:", error);
            setToastMessage("An error occurred while logging out."); // Show error toast
            setTimeout(() => setToastMessage(null), 3000); // Hide toast after 3 seconds
        }
    };

    return (
        <div className="home-container">
            <h3 className={status === "error" ? "error-text" : "success-text"}>
                {message}
            </h3>
            {status === "success" && (
                <button onClick={handleLogout} className="logout-btn">
                    Logout
                </button>
            )}
            {toastMessage && (
                <div className="toast">
                    {toastMessage}
                </div>
            )}
        </div>
    );
};

export default Home;
