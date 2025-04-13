import React, { useEffect, useState } from "react";
import axios from "axios";
import "./User_Orders.css";

interface OrderItem {
  flavor_id: number;
  quantity: number;
  price: number;
  flavor_name?: string;
}

interface Order {
  order_id: number;
  total_price: number;
  created_at: string;
  items: OrderItem[];
}

const UserOrders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const rowsPerPage = 3;

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/ordersFromUser",
          {
            withCredentials: true,
          }
        );
        const { data } = response;

        if (data.status === "success") {
          setOrders(data.orders);
        } else {
          setError(data.message);
        }
      } catch (err: any) {
        setError(
          err.response?.data?.message || "An unexpected error occurred."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  const fetchFlavorNames = async (order: Order) => {
    try {
      const updatedItems = await Promise.all(
        order.items.map(async (item) => {
          const response = await axios.post(
            "http://localhost:8000/searchFlavorById",
            { id: item.flavor_id }
          );
          return {
            ...item,
            flavor_name: response.data?.data?.name || "Unknown",
          };
        })
      );
      setSelectedOrder({ ...order, items: updatedItems });
    } catch (error) {
      alert("Failed to fetch flavor names.");
    }
  };

  const totalPages = Math.ceil(orders.length / rowsPerPage);

  const handlePrevious = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };

  const handleNext = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  };

  const startIndex = (currentPage - 1) * rowsPerPage;
  const endIndex = startIndex + rowsPerPage;
  const currentOrders = orders.slice(startIndex, endIndex);

  if (loading) return <p>Loading your orders...</p>;

  if (error)
    return <p style={{ color: "blue", textAlign: "center" }}>{error}</p>;

  const closeModal = () => setSelectedOrder(null);

  const convertToIST = (dateString: string) => {
    const utcDate = new Date(dateString); // Parse the UTC date string
    const istOffset = 5.5 * 60; // IST is UTC+5:30, in minutes
    const localTime = utcDate.getTime() + istOffset * 60 * 1000; // Add offset in milliseconds
    return new Date(localTime).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "medium",
      hour12: true, // For "am/pm" format
    });
  };

  return (
    <div className="user-orders-container-head">
      {orders.length === 0 ? (
        <p>No orders found. Start ordering your favorite flavors!</p>
      ) : (
        <div>
          <div className="user-orders-container-body">
            {currentOrders.map((order) => (
              <div
                key={order.order_id}
                className="user-orders-container-body-details"
              >
                <p>
                  <strong>Order #{order.order_id}</strong>
                  <br />
                  <button
                    className="toggle-details-button"
                    onClick={() => fetchFlavorNames(order)}
                  >
                    Show Details
                  </button>
                </p>
                <p>Placed on: {convertToIST(order.created_at)}</p>
                <p>Total Price: ${Number(order.total_price).toFixed(2)}</p>
              </div>
            ))}
          </div>
          <div className="pagination-controls">
            <button onClick={handlePrevious} disabled={currentPage === 1}>
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages}
            </span>
            <button onClick={handleNext} disabled={currentPage === totalPages}>
              Next
            </button>
          </div>
        </div>
      )}

      {selectedOrder && (
        <div className="modal">
          <div className="modal-content">
            <button className="close-button" onClick={closeModal}>
              ×
            </button>
            <h3>Order Details</h3>
            <p>
              <strong>Order #{selectedOrder.order_id}</strong>
            </p>
            <p>
              <p>Placed on: {convertToIST(selectedOrder.created_at)}</p>
            </p>
            <p>Total Price: ${Number(selectedOrder.total_price).toFixed(2)}</p>
            <table className="user-orders-container-body-table">
              <thead>
                <tr>
                  <th>Flavor ID</th>
                  <th>Name</th>
                  <th>Quantity</th>
                  <th>Price</th>
                </tr>
              </thead>
              <tbody>
                {selectedOrder.items.map((item, index) => (
                  <tr key={index}>
                    <td>{item.flavor_id}</td>
                    <td>{item.flavor_name || "Fetching..."}</td>
                    <td>{item.quantity}</td>
                    <td>${Number(item.price).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserOrders;
