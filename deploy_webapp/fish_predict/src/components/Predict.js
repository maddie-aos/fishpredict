// Import necessary dependencies
import React from 'react';
import { Routes, Link, Route, useNavigate } from 'react-router-dom';
import './main.css';
import CitSor from './species/citsor';
import EngMor from './species/engmor';
import ParCal from './species/parcal';
import ScoJap from './species/scojap';
import ThuAla from './species/thuala';
import XipGla from './species/xipgla';

// Define the Predict component
function Predict() {
  const navigate = useNavigate(); // Get the navigate function from react-router-dom

  return (
    <div className="page-container">
      <h1 align="center">Select Species</h1>
      <nav>
        <ul>
          {/* Add a back link to the homepage */}
          <li><Link to="/" className="nav-link">Back to Home</Link></li>
        </ul>
      </nav>
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
        <Route path="/cit_sor" element={<CitSor />} />
        <Route path="/eng_mor" element={<EngMor />} />
        <Route path="/par_cal" element={<ParCal />} />
        <Route path="/sco_jap" element={<ScoJap />} />
        <Route path="/thu_ala" element={<ThuAla />} />
        <Route path="/xip_gla" element={<XipGla />} />
        {/* Add routes for other species if needed */}
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
