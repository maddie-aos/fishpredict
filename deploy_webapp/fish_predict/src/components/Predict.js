// Import necessary dependencies
import React from 'react';
import { Routes, Link } from 'react-router-dom';
import './main.css';

// Define the Predict component
function Predict() {
  return (
    <div className="page-container">
      {/* Add a link to the homepage */}
      <nav>
          <ul>
            <li><Link to="/" className="nav-link">Home</Link></li>
          </ul>
        </nav>

      <h1 align="center">Select Species</h1>
      <div className="button">
        <div className="button-container">
          <Link to="/cit_sor" className="grey-button">Pacific Sanddab (Citharichthys sordidus)</Link>
          <Link to="/eng_mor" className="grey-button">Northern Anchovy (Engraulis mordax)</Link>
          <Link to="/par_cal" className="grey-button">California Halibut (Paralichthys californicus)</Link>
        </div>
      </div>
      <div className="button">
        <div className="button-container">
          <Link to="/sco_jap" className="grey-button">Chub Mackerel (Scomber japonicus)</Link>
          <Link to="/thu_ala" className="grey-button">Albacore Tuna (Thunnus alalunga)</Link>
          <Link to="/xip_gla" className="grey-button">Pacific Swordfish (Xiphias gladius)</Link>
        </div>
      </div>
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cit_sor" element={<Predict />} />
          <Route path="/dedication" element={<Dedication />} />
        </Routes>
      <footer>
        <div className="footer-content">
          <p>&copy; 2024 Madeline Smith. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

// Export the Predict component
export default Predict;



