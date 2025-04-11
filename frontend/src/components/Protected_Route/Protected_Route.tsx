import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/", {
            method: "GET",
            credentials: "include",
        })
            .then((response) => {
                if (response.status === 403) {
                    setIsAuthenticated(false);
                } else {
                    setIsAuthenticated(true);
                }
            })
            .catch(() => setIsAuthenticated(false));
    }, []);

    if (isAuthenticated === null) {
        return <div>Loading...</div>; // Show a loading spinner or placeholder
    }

    return isAuthenticated ? children : <Navigate to="/login" replace />;
};

export default ProtectedRoute;
