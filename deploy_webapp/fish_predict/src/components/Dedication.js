// Dedication.js
import React from 'react';
import './main.css';
import { Link, useNavigate } from 'react-router-dom';
import PapaFishingImage from '/Users/maddie/Projects/fishpredict/deploy_webapp/fish_predict/src/components/papa_fishing.jpg';

function Dedication() {
  const navigate = useNavigate(); // Get the navigate function from react-router-dom

  return (
    
    <div className="page-container">

      <h1 align="center">For Papa</h1>
      <nav>
        <ul>
          {/* Add a back link to the homepage */}
          <li><Link to="/" className="nav-link">Back to Home</Link></li>
        </ul>
      </nav>

      {/* Display the image */}
      <div className="image-container">
        <img src={PapaFishingImage} alt="Papa Fishing" />
        <p>
          Thanks for teaching me how to love the ocean, hope you're catching all the tuna up in Heaven!
        </p>
      </div>

      {/* Dedication component content */}
      <footer>
        <div className="footer-content">
          <p>&copy; 2024 Madeline Smith. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default Dedication;
