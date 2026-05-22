"use client";

import React, { useState } from "react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
    setIsOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <span className="navbar-logo" onClick={() => scrollToSection("hero")}>
          The Indian Fashion Forecasting Lab
        </span>
        
        {/* Desktop Links only */}
        <div className="navbar-links desktop-only">
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

        {/* Hamburger Icon */}
        <button 
          type="button"
          className={`hamburger-menu ${isOpen ? "open" : ""}`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation menu"
        >
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </button>
      </div>

      {/* Mobile Links Dropdown */}
      <div className={`mobile-nav-menu ${isOpen ? "open" : ""}`}>
        <button 
          type="button" 
          className="mobile-nav-link" 
          onClick={() => scrollToSection("forecaster")}
        >
          Forecaster
        </button>
        <button 
          type="button" 
          className="mobile-nav-link" 
          onClick={() => scrollToSection("moodboards")}
        >
          Instagram Trends
        </button>
        <button 
          type="button" 
          className="mobile-nav-link" 
          onClick={() => scrollToSection("about-project")}
        >
          About the Model
        </button>
      </div>
    </nav>
  );
}

