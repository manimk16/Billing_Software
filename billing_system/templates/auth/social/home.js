
import React from 'react';
import { Link } from 'react-router-dom';
import './home.css'; // Optional CSS file for styling

const HomePage = () => {
    return (
        <div className="home-container">
            <header>
                <h1>Welcome to the Billing System</h1>
                <nav>
                    <ul>
                        <li><Link to="/invoices">Invoices</Link></li>
                        <li><Link to="/clients">Clients</Link></li>
                        <li><Link to="/payments">Payments</Link></li>
                    </ul>
                </nav>
            </header>
            <main>
                <section>
                    <h2>Features</h2>
                    <p>Manage your invoices, clients, and payments easily.</p>
                </section>
            </main>
            <footer>
                <p>&copy; 2024 Your Company Name</p>
            </footer>
        </div>
    );
};

export default HomePage;
