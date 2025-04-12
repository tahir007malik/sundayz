import React, { useEffect, useState } from "react";
import axios from "axios";
import "./User_Orders.css";

interface OrderItem {
    flavor_id: number;
    quantity: number;
    price: number;
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

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get("http://localhost:8000/ordersFromUser", {
                    withCredentials: true,
                });
                const { data } = response;

                if (data.status === "success") {
                    setOrders(data.orders);
                } else {
                    setError(data.message);
                }
            } catch (err: any) {
                setError(err.response?.data?.message || "An unexpected error occurred.");
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    if (loading) return <p>Loading your orders...</p>;

    if (error) return <p style={{ color: "blue", textAlign: "center" }}>{error}</p>;

    const closeModal = () => setSelectedOrder(null);

    return (
        <div className="user-orders-container-head">
            {orders.length === 0 ? (
                <p>No orders found. Start ordering your favorite flavors!</p>
            ) : (
                <div className="user-orders-container-body">
                    {orders.map((order) => (
                        <div key={order.order_id} className="user-orders-container-body-details">
                            <p>
                                <strong>Order #{order.order_id}</strong><br />
                                <button
                                    className="toggle-details-button"
                                    onClick={() => setSelectedOrder(order)}
                                >
                                    Show Details
                                </button>
                            </p>
                            <p>Placed on: {new Date(order.created_at).toLocaleString()}</p>
                            <p>Total Price: ${Number(order.total_price).toFixed(2)}</p>
                        </div>
                    ))}
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
                        <p>Placed on: {new Date(selectedOrder.created_at).toLocaleString()}</p>
                        <p>Total Price: ${Number(selectedOrder.total_price).toFixed(2)}</p>
                        <table className="user-orders-container-body-table">
                            <thead>
                                <tr>
                                    <th>Flavor ID</th>
                                    <th>Quantity</th>
                                    <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {selectedOrder.items.map((item, index) => (
                                    <tr key={index}>
                                        <td>{item.flavor_id}</td>
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
