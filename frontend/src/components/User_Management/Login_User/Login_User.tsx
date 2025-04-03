import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Login_User.css";

const Login = () => {
    const [formData, setFormData] = useState({ email: "", password: "" });
    const [message, setMessage] = useState("");
    const [showPopup, setShowPopup] = useState(false);
    const navigate = useNavigate(); // Hook for redirection

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMessage("Logging in...");
        setShowPopup(true); // Show popup immediately when login starts

        try {
            const response = await fetch("http://localhost:8000/loginUser", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            const data = await response.json();
            setMessage(data.message);
            setShowPopup(true); // Ensure pop-up displays

            if (response.ok) {
                setTimeout(() => {
                    setShowPopup(false);
                    navigate(data.redirect_url); // Redirect to home
                }, 1500);
            }
        } catch (error) {
            setMessage("Error: Unable to login");
            setShowPopup(true);
        }
    };

    const closePopup = () => {
        setShowPopup(false);
    };

    return (
        <div className="login-container">
            <h2>Login</h2><br />
            <form onSubmit={handleSubmit}>
                <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
                <button type="submit">Login</button>
            </form><br />
            <p className="signup-link">
                Create a new account here! <Link to="/signup">Signup</Link>
            </p>

            {/* Popup Modal */}
            {showPopup && (
                <div className="popup">
                    <div className="popup-content">
                        <span className="close-btn" onClick={closePopup}>&times;</span>
                        <p>{message}</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Login;
