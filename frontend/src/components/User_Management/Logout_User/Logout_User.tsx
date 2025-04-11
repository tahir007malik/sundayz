import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Logout = () => {
    const navigate = useNavigate();
    const [toastMessage, setToastMessage] = useState<string | null>(null); // State for toast message

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
        <>
            <button onClick={handleLogout} className="logout-btn">
                Logout
            </button>
            {toastMessage && (
                <div className="toast">
                    {toastMessage}
                </div>
            )}
        </>
    );
};

export default Logout;
