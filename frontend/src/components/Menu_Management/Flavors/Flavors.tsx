import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Flavors.css';

const Flavors: React.FC = () => {
    const [flavors, setFlavors] = useState<any[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [currentPage, setCurrentPage] = useState<number>(1);
    const rowsPerPage = 5;

    useEffect(() => {
        const fetchFlavors = async () => {
            try {
                const response = await axios.get('http://localhost:8000/getAllFlavors');
                setFlavors(response.data);
            } catch (err: any) {
                setError(
                    err.response?.data?.message || 'An error occurred while fetching the flavors.'
                );
            } finally {
                setLoading(false);
            }
        };
        fetchFlavors();
    }, []);

    const totalPages = Math.ceil(flavors.length / rowsPerPage);

    const handlePrevious = () => {
        setCurrentPage((prev) => Math.max(prev - 1, 1));
    };

    const handleNext = () => {
        setCurrentPage((prev) => Math.min(prev + 1, totalPages));
    };

    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const currentFlavors = flavors.slice(startIndex, endIndex);

    if (loading) return <p>Loading...</p>;

    if (error) {
        return (
            <div className="error-alert">
                <h4>Error</h4>
                <p>{error}</p>
            </div>
        );
    }

    if (flavors.length === 0) {
        return (
            <div className="no-flavors-alert">
                <h4>No Flavors Available</h4>
                <p>There are currently no flavors in the database.</p>
            </div>
        );
    }

    return (
        <div className="flavors-table-container">
            <table className="flavors-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Available</th>
                    </tr>
                </thead>
                <tbody>
                    {currentFlavors.map((flavor) => (
                        <tr key={flavor.id}>
                            <td>{flavor.id}</td>
                            <td>{flavor.name}</td>
                            <td>${flavor.price.toFixed(2)}</td>
                            <td>{flavor.quantity}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
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
    );
};

export default Flavors;
