"use client";

import React from "react";

export default function AboutSection() {
  return (
    <div id="about-project" className="box about-box">
      <h2>About the Forecasting Model</h2>
      <p className="about-intro">
        The Indian Fashion Forecasting Lab is a state-of-the-art predictive intelligence platform 
        tailored for designers, retail buyers, and garment manufacturers. By combining live cultural 
        signals with advanced machine learning, we bridge the gap between digital sentiment and commercial production.
      </p>

      <div className="about-grid">
        {/* Core Methodology Cards */}
        <div className="about-card">
          <div className="card-header-icon">✦</div>
          <h3>Cultural Signal Cultivation</h3>
          <p>
            We query real-time search velocity, interest peaks, and social media trends across Google and Pinterest. 
            By capturing micro-trends as they arise, our system accurately measures cultural momentum before it hits mainstream retail.
          </p>
        </div>

        <div className="about-card">
          <div className="card-header-icon">✦</div>
          <h3>Generative Fashion Intelligence</h3>
          <p>
            Powered by Google Gemini 2.0 AI, our analytical engine translates raw digital scores into comprehensive WGSN-grade forecasts. 
            Every trend is contextualized with demographic targeting, competitor movements, and peak seasonal timelines.
          </p>
        </div>

        <div className="about-card">
          <div className="card-header-icon">✦</div>
          <h3>Budget &amp; Risk Mitigation</h3>
          <p>
            To prevent overproduction and inventory deadweight, the model generates custom investment allocation percentages 
            and safety signals (e.g., &quot;Strong Buy&quot;, &quot;Hold&quot;, &quot;Avoid&quot;) aligned with the specific risks of the Indian market.
          </p>
        </div>

        <div className="about-card">
          <div className="card-header-icon">✦</div>
          <h3>Upstash Redis Cache Layer</h3>
          <p>
            Computational trends are cached via a high-performance Redis cache for 24 hours. 
            This optimizes server response times to under 10ms while ensuring consistent and stable analytical retrieval.
          </p>
        </div>
      </div>

      <div className="about-stats-panel">
        <div className="stat-item">
          <span className="stat-number">98%</span>
          <span className="stat-label">Model Confidence Peak</span>
        </div>
        <div className="stat-divider"></div>
        <div className="stat-item">
          <span className="stat-number">70+</span>
          <span className="stat-label">Aesthetics Monitored</span>
        </div>
        <div className="stat-divider"></div>
        <div className="stat-item">
          <span className="stat-number">Real-Time</span>
          <span className="stat-label">Google Trends Live API</span>
        </div>
      </div>
    </div>
  );
}
