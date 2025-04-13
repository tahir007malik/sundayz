import React, { useState } from "react";
import './Create_Order.css';

const CreateOrder = () => {
    const [flavorId, setFlavorId] = useState<number | null>(null);
    const [quantity, setQuantity] = useState<number | null>(null);
    const [toastMessage, setToastMessage] = useState<string | null>(null);

    const handleCreateOrder = async () => {
        if (!flavorId || !quantity) {
            setToastMessage("Both Flavor ID and Quantity are required.");
            return;
        }

        const payload = {
            user_id: 1, // Replace with the actual logged-in user ID
            items: [{ flavor_id: flavorId, quantity }],
        };

        try {
            const response = await fetch("http://localhost:8000/createOrder", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const data = await response.json();
            setToastMessage(data.message);
        } catch (error) {
            console.error("Error creating order:", error);
            setToastMessage("Failed to create order. Please try again.");
        }
    };

    return (
        <div>
            <h5>Create Order</h5>
            <input
                type="number"
                placeholder="Flavor ID"
                value={flavorId || ""}
                onChange={(e) => setFlavorId(Number(e.target.value))}
            />
            <input
                type="number"
                placeholder="Quantity"
                value={quantity || ""}
                onChange={(e) => setQuantity(Number(e.target.value))}
            />
            <button onClick={handleCreateOrder}>Place Order</button>
            {toastMessage && <div className="toast">{toastMessage}</div>}
        </div>
    );
};

export default CreateOrder;
