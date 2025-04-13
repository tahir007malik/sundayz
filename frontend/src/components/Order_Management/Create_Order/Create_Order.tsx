import React, { useState } from "react";
import axios from "axios";
import "./Create_Order.css";

interface OrderItem {
  flavor_id: number;
  flavor_name?: string;
  quantity: number;
  total_price?: string;
}

const CreateOrder: React.FC = () => {
  const [items, setItems] = useState<OrderItem[]>([]);
  const [showPopup, setShowPopup] = useState(false);
  const [currentItem, setCurrentItem] = useState<OrderItem>({
    flavor_id: 1,
    quantity: 1,
  });
  const [showOrderSummary, setShowOrderSummary] = useState(false);
  const handleAddItem = async () => {
    if (currentItem.flavor_id <= 0 || currentItem.quantity <= 0) {
      alert("Please enter a valid flavor ID and quantity.");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/searchFlavorById",
        { id: currentItem.flavor_id }
      );

      const { data: flavorDetails } = response.data;

      if (flavorDetails) {
        const flavorName = flavorDetails.name;
        const pricePerUnit = flavorDetails.price;
        const totalPrice = (pricePerUnit * currentItem.quantity).toFixed(2);

        const updatedItem = {
          ...currentItem,
          flavor_name: flavorName,
          total_price: totalPrice,
        };

        setItems([...items, updatedItem]);
        setCurrentItem({ flavor_id: 1, quantity: 1 });
      } else {
        alert("Flavor details not found.");
      }
    } catch (error: any) {
      alert(error.response?.data?.message || "Failed to fetch flavor details.");
    }
  };

  const handleRemoveItem = (index: number) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const handlePlaceOrder = async () => {
    if (items.length === 0) {
      alert("Please add at least one item to your order.");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/createOrder",
        { items },
        { withCredentials: true }
      );

      const { message, order_details } = response.data;

      if (order_details && order_details.length > 0) {
        const updatedItems = order_details.map((detail: any) => ({
          flavor_id: detail.flavor_id,
          flavor_name: detail.flavor_name,
          quantity: detail.quantity,
          total_price: detail.total_price,
        }));

        setItems(updatedItems);
        alert(message || "Order placed successfully!");
        setShowOrderSummary(true);
      } else {
        alert("No order details found.");
      }
    } catch (error: any) {
      alert(error.response?.data?.message || "Failed to place order.");
    }
  };

  return (
    <div className="create-order-container-component-body">
      <button
        className="custom-button center-button"
        onClick={() => setShowPopup(true)}
      >
        Make an order
      </button>

      {showPopup && (
        <div className="modal-create-order">
          <div className="modal-create-order-content">
            <button
              className="close-button-create-order"
              onClick={() => setShowPopup(false)}
              aria-label="Close"
            >
              ✖
            </button>

            <label className="create-order-modal-label">Flavor ID</label>
            <br />
            <input
              type="text"
              placeholder="Flavor ID"
              className="create-order-input-field"
              value={currentItem.flavor_id === 0 ? "" : currentItem.flavor_id}
              onChange={(e) => {
                const value = e.target.value.replace(/[^0-9]/g, "");
                setCurrentItem({
                  ...currentItem,
                  flavor_id: value === "" ? 0 : parseInt(value),
                });
              }}
            />
            <br />
            <br />

            <label className="create-order-modal-label">Quantity</label>
            <br />
            <input
              type="text"
              placeholder="Quantity"
              className="create-order-input-field"
              value={currentItem.quantity === 0 ? "" : currentItem.quantity}
              onChange={(e) => {
                const value = e.target.value.replace(/[^0-9]/g, "");
                setCurrentItem({
                  ...currentItem,
                  quantity: value === "" ? 0 : parseInt(value),
                });
              }}
            />
            <br />
            <br />

            <button className="custom-button secondary" onClick={handleAddItem}>
              Add to Cart
            </button>
            <br />
            <br />

            <button
              className="custom-button"
              onClick={() => setShowOrderSummary(true)}
            >
              View Order Summary
            </button>
            <br />
            <br />

            {showOrderSummary && (
              <div className="modal-content-order-summary">
                <h4>Order Summary</h4>
                <table className="user-orders-container-body-table">
                  <thead>
                    <tr>
                      <th>Flavor ID</th>
                      <th>Name</th>
                      <th>Quantity</th>
                      <th>Total Price</th>
                      <th>Operation</th>
                    </tr>
                  </thead>
                  <tbody>
                    {items.map((item, index) => (
                      <tr key={index}>
                        <td>{item.flavor_id}</td>
                        <td>{item.flavor_name || "Fetching..."}</td>
                        <td>{item.quantity}</td>
                        <td>{item.total_price || "Calculating..."}</td>
                        <td>
                          <button
                            className="remove-item-button"
                            onClick={() => handleRemoveItem(index)}
                            aria-label="Remove Item"
                          >
                            ✖
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <br />
                <br />

                <button
                  className="custom-button"
                  onClick={handlePlaceOrder}
                  disabled={items.length === 0}
                >
                  Place Order
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CreateOrder;
