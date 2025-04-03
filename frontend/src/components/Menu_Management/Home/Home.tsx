import React, { useEffect, useState } from "react";

const Home = () => {
    const [message, setMessage] = useState("Loading...");

    useEffect(() => {
        fetch("http://localhost:8000/")
            .then((response) => response.json())
            .then((data) => setMessage(data.message))
            .catch(() => setMessage("Error loading data"));
    }, []);

    return (
        <div className="home-container">
            <h1>{message}</h1>
        </div>
    );
};

export default Home;
