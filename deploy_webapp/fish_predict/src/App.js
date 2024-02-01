// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './main.css';
import Home from './components/Home';
import Predict from './components/Predict';
import Dedication from './components/Dedication';

function App() {
  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/dedication" element={<Dedication />} />
      </Routes>
    </Router>
  );
}

export default App;
