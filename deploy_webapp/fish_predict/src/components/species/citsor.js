// Import necessary dependencies
import React from 'react';
import { Link } from 'react-router-dom';
import './main.css';

// Define the CitSor component
function CitSor() {
  return (
    <div className="page-container">
      {/* Add a styled link to the homepage */}
      <Link to="/" className="grey-button home-link">Home</Link>

      <h1 align="center">Enter Latitude and Longitude Data</h1>
      <div className="button" style={{ display: 'block', marginBottom: 0, marginRight: '10px' }}>
        <div id="input" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '10px' }}>
          <form action="/cit_sor_pred" method="post" className="info">
            <input type="text" name="latitudechange" placeholder="32.555" />
            <input type="text" name="longitudechange" placeholder="-118.004" />
          </form>
        </div>
      </div>
      <div className="button" style={{ display: 'block', marginBottom: 0, marginRight: '10px' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '10px' }}>
          <form action="/cit_sor_pred" method="post" className="info">
            <button className="submit">Predict</button>
          </form>
        </div>
      </div>
      <div className="centered-box">
        <p className="coordinates">Sample Ocean Coordinates: 32.555, -118.004</p>
        <p className="coordinates">Sample Land Coordinates: 24.748, 39.807</p>
        <p className="coordinates">Sample Invalid Coordinates: 99.660, -189.004</p>
      </div>
      <footer>
        <p>&copy; 2024 Madeline Smith. All rights reserved.</p>
      </footer>
    </div>
  );
}

// Export the CitSor component
export default CitSor;
