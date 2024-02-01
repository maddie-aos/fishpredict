// Home.js
import React from 'react';
import './main.css';
import { Routes, Route, Link } from 'react-router-dom';
import Predict from './Predict';
import Dedication from './Dedication';

function Home() {
  return (
    <div className="page-container">
      <nav>
        <ul>
          <h1>Welcome!</h1>
          <li><Link to="/predict" className="nav-link">Make a Prediction</Link></li>
          <li><Link to="/dedication" className="nav-link">Dedication</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/predict" element={<Predict />} />
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

export default Home;
