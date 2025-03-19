import React from "react";
import './TopNavBar.css';

const TopNavBar = () => {
  return (
    <nav className="navigation-bar">
      <div className="app-name">My App</div>
      <div className="links-container">
        <a href="/" className="link">Home</a>
        <a href="/about" className="link">About</a>
        <a href="/search" className="link">Search</a>
      </div>
    </nav>
  );
};

export default TopNavBar;
