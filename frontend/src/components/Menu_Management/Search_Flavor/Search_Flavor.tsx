import React, { useState } from "react";
import axios from "axios";
import "./Search_Flavor.css";

const SearchFlavor: React.FC = () => {
    const [searchInput, setSearchInput] = useState<string>(""); // To track user input
    const [flavor, setFlavor] = useState<any | null>(null); // To store the fetched flavor data
    const [error, setError] = useState<string | null>(null); // To handle error messages
    const [loading, setLoading] = useState<boolean>(false); // Loading state

    const handleSearch = async () => {
        if (!searchInput.trim()) {
            setError("Please enter a valid flavor name.");
            return;
        }

        setLoading(true);
        setError(null);
        setFlavor(null); // Reset previous results

        try {
            const response = await axios.post("http://localhost:8000/searchFlavor", {
                name: searchInput.trim(),
            });

            if (response.data.status === "success") {
                setFlavor(response.data.data[0]); // API returns an array with one object
            } else {
                setError(response.data.message || "An unexpected error occurred.");
            }
        } catch (err: any) {
            setError(
                err.response?.data?.message ||
                "An error occurred while searching for the flavor."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="search-flavor-container">
            {/* <h3>Search Flavor</h3> */}
            <div className="search-input-container">
                <input
                    type="text"
                    placeholder="Enter flavor name"
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    className="search-input"
                />
                <button onClick={handleSearch} className="search-button">
                    {loading ? "Searching..." : "Search"}
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            {flavor && (
                <div className="flavor-result">
                    {/* <h4>Flavor Details</h4> */}
                    <table className="flavor-details-table">
                        <tbody>
                            <tr>
                                <td>ID:</td>
                                <td>{flavor.id}</td>
                            </tr>
                            <tr>
                                <td>Name:</td>
                                <td>{flavor.name}</td>
                            </tr>
                            <tr>
                                <td>Price:</td>
                                <td>${flavor.price.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Quantity:</td>
                                <td>{flavor.quantity}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default SearchFlavor;
