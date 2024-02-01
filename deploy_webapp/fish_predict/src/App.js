import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './main.css';
import Home from './components/Home';
import Predict from './components/Predict';
import Dedication from './components/Dedication';

function App() {
  return (
    <Router>
      <div className="page-container">
        <h1>Welcome!</h1>
        <nav>
          <ul>
            <li><Link to="/predict" className="nav-link">Make a Prediction</Link></li>
            <li><Link to="/dedication" className="nav-link">Dedication</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/dedication" element={<Dedication />} />
        </Routes>
        <footer>
          <div className="footer-content">
            <p>&copy; 2024 Madeline Smith. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
