import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import Flavors from "../Flavors/Flavors.tsx";
import SearchFlavor from "../Search_Flavor/Search_Flavor.tsx";
import UserOrders from "../../Order_Management/User_Orders/User_Orders.tsx";
import CreateOrder from "../../Order_Management/Create_Order/Create_Order.tsx";

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
      .then((response) => {
        if (response.status === 403) {
          setToastMessage("Unauthorized access."); // Show unauthorized access toast
          setStatus("error");
          throw new Error("Unauthorized"); // Prevent further processing
        }
        return response.json();
      })
      .then((data) => {
        setMessage(data.message); // Set the message from backend
        setStatus(data.status);
      })
      .catch((error) => {
        if (error.message !== "Unauthorized") {
          setToastMessage("An unexpected error occurred."); // Show error toast
          setStatus("error");
        }
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
      <div className="home-container-header">
        <h3 className={status === "error" ? "error-text" : "success-text"}>
          {message}
        </h3>
        {status === "success" && (
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        )}
      </div>
      <div className="home-body-container">
        <div className="flavors-container">
          <h4>Flavors</h4>
          <Flavors />
        </div>
        <div className="vertical-split-container">
          <div className="create-order-container">
            <h4>Create Order</h4>
            <CreateOrder />
          </div>
          <br /> <br /> <br />
          <div className="search-flavors-container">
            <h4>Search Flavor</h4>
            <SearchFlavor />
          </div>
        </div>
        <div className="user-orders-container">
          <h4>My Orders</h4>
          <UserOrders />
        </div>
      </div>
      {toastMessage && (
        <div className="toast">
          {toastMessage}
          <button
            onClick={() => setToastMessage(null)}
            className="toast-close-btn"
          >
            ✖
          </button>
        </div>
      )}
    </div>
  );
};

export default Home;
