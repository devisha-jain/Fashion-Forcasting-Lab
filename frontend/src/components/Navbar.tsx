"use client";

import React from "react";

export default function Navbar() {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <span className="navbar-logo" onClick={() => scrollToSection("hero")}>
          Fashion Forecasting Lab
        </span>
        <div className="navbar-links">
          <button 
            type="button" 
            className="nav-link" 
            onClick={() => scrollToSection("forecaster")}
          >
            Forecaster
          </button>
          <button 
            type="button" 
            className="nav-link" 
            onClick={() => scrollToSection("moodboards")}
          >
            Instagram Trends
          </button>
          <button 
            type="button" 
            className="nav-link nav-link-about" 
            onClick={() => scrollToSection("about-project")}
          >
            About the Model
          </button>
        </div>
      </div>
    </nav>
  );
}
