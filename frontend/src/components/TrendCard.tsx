"use client";

import { useEffect, useRef, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LineElement,
  LineController,
  PointElement,
  BarElement,
  BarController,
  ArcElement,
  DoughnutController,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  LineController,
  PointElement,
  BarElement,
  BarController,
  ArcElement,
  DoughnutController,
  Filler,
  Tooltip,
  Legend
);

const CHART_COLORS = [
  "#cba89a", // baby pink/nude
  "#8b5a2b", // rich brown
  "#d2b48c", // beige
  "#50352d"  // dark brown
];

interface TrendCardProps {
  trend: {
    name: string;
    confidence: number;
    description: string;
    business: string;
    momentum: string;
    palette: string[];
    graph: Record<string, number>;
    demographics: Record<string, number>;
    image: string;
    images?: string[];
    sources: string[];
    investSignal?: string;
    investPercent?: number;
    investReason?: string;
    yearlyForecast?: Array<{ year: string; score: number }>;
    risks?: string;
    targetDemographic?: string;
    peakSeason?: string;
    competitorActivity?: string;
  };
  index: number;
  cached: boolean;
}

const SIGNAL_CONFIG: Record<string, { label: string; color: string; bg: string; border: string; dot: string }> = {
  "Strong Buy": {
    label: "Strong Buy",
    color: "#2e7d32",
    bg: "#e8f5e9",
    border: "rgba(46, 125, 50, 0.3)",
    dot: "#2e7d32",
  },
  "Moderate Buy": {
    label: "Moderate Buy",
    color: "#2e7d32",
    bg: "#edf7ed",
    border: "#c2e7c4",
    dot: "#2e7d32",
  },
  Hold: {
    label: "Hold",
    color: "#d97706",
    bg: "#fffbeb",
    border: "#fef3c7",
    dot: "#d97706",
  },
  Avoid: {
    label: "Avoid",
    color: "#dc2626",
    bg: "#fef2f2",
    border: "#fee2e2",
    dot: "#dc2626",
  },
};

export default function TrendCard({ trend, index, cached }: TrendCardProps) {
  const lineRef = useRef<HTMLCanvasElement>(null);
  const lineChartRef = useRef<ChartJS | null>(null);

  const barRef = useRef<HTMLCanvasElement>(null);
  const barChartRef = useRef<ChartJS | null>(null);

  const pieRef = useRef<HTMLCanvasElement>(null);
  const pieChartRef = useRef<ChartJS | null>(null);

  const [imagesLoaded, setImagesLoaded] = useState<boolean[]>([false, false, false]);
  const [lightboxSrc, setLightboxSrc] = useState<string | null>(null);

  const getSignalConfig = (signal: string | undefined) => {
    const s = signal?.trim().toLowerCase() || "hold";
    if (s.includes("strong") && s.includes("buy")) return SIGNAL_CONFIG["Strong Buy"];
    if (s.includes("moderate") && s.includes("buy")) return SIGNAL_CONFIG["Moderate Buy"];
    if (s.includes("avoid")) return SIGNAL_CONFIG["Avoid"];
    return SIGNAL_CONFIG["Hold"];
  };

  const signalConfig = getSignalConfig(trend.investSignal);
  const investPercent = trend.investPercent ?? 18;

  // Yearly projection line chart
  useEffect(() => {
    if (!lineRef.current || !trend.yearlyForecast?.length) return;
    if (lineChartRef.current) lineChartRef.current.destroy();
    const ctx = lineRef.current.getContext("2d");
    if (!ctx) return;

    const gradient = ctx.createLinearGradient(0, 0, 0, 160);
    gradient.addColorStop(0, "rgba(203, 168, 154, 0.25)");
    gradient.addColorStop(1, "rgba(203, 168, 154, 0.01)");

    // Custom inline plugin to draw labels directly on top of the points
    const datalabelsPlugin = {
      id: "datalabels",
      afterDatasetsDraw(chart: ChartJS) {
        const { ctx, data } = chart;
        ctx.save();
        ctx.font = "bold 11px Inter, sans-serif";
        ctx.fillStyle = "#8b5a2b";
        ctx.textAlign = "center";
        ctx.textBaseline = "bottom";

        chart.getDatasetMeta(0).data.forEach((point: unknown, idx: number) => {
          const p = point as { x: number; y: number };
          const value = data.datasets[0].data[idx];
          if (value !== undefined && value !== null) {
            ctx.fillText(value.toString(), p.x, p.y - 8);
          }
        });
        ctx.restore();
      }
    };

    lineChartRef.current = new ChartJS(ctx, {
      type: "line",
      data: {
        labels: trend.yearlyForecast.map((d) => d.year),
        datasets: [
          {
            label: "Trend Score",
            data: trend.yearlyForecast.map((d) => d.score),
            borderColor: "#cba89a",
            backgroundColor: gradient,
            borderWidth: 2,
            pointBackgroundColor: "#8b5a2b",
            pointBorderColor: "#ffffff",
            pointBorderWidth: 1.5,
            pointRadius: 5.5,
            pointHoverRadius: 7,
            tension: 0.2, // Clean, slight curves
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 20, // Add padding at the top so labels don't get cut off
            bottom: 5,
            left: 10,
            right: 10
          }
        },
        scales: {
          y: { 
            display: false, // Hide Y-axis completely as in screenshot
            beginAtZero: false, 
            min: 0, 
            max: 110 // Elevated so labels fit nicely
          },
          x: { 
            grid: { display: false },
            ticks: {
              color: "#8b5a2b",
              font: {
                family: "Inter",
                size: 11,
                weight: "normal"
              }
            },
            border: { display: false }
          },
        },
        plugins: { 
          legend: { display: false },
          tooltip: { enabled: true }
        },
      },
      plugins: [datalabelsPlugin]
    });

    return () => {
      if (lineChartRef.current) lineChartRef.current.destroy();
    };
  }, [trend.yearlyForecast]);

  // Bar Chart (Signal Strength)
  useEffect(() => {
    if (!barRef.current || !trend.graph) return;
    if (barChartRef.current) barChartRef.current.destroy();
    const ctx = barRef.current.getContext("2d");
    if (!ctx) return;

    const labels = Object.keys(trend.graph);
    const dataValues = Object.values(trend.graph);

    barChartRef.current = new ChartJS(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Signal Strength",
            data: dataValues,
            backgroundColor: CHART_COLORS,
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: "rgba(139, 90, 43, 0.05)",
            },
            ticks: {
              color: "#8b5a2b",
              font: {
                family: "Inter",
                size: 10,
              },
            },
            border: { display: false },
          },
          x: {
            grid: { display: false },
            ticks: {
              color: "#8b5a2b",
              font: {
                family: "Inter",
                size: 11,
              },
            },
            border: { display: false },
          },
        },
        plugins: {
          legend: { display: false },
          tooltip: { enabled: true },
        },
      },
    });

    return () => {
      if (barChartRef.current) barChartRef.current.destroy();
    };
  }, [trend.graph]);

  // Doughnut Chart (Demographics)
  useEffect(() => {
    if (!pieRef.current || !trend.demographics) return;
    if (pieChartRef.current) pieChartRef.current.destroy();
    const ctx = pieRef.current.getContext("2d");
    if (!ctx) return;

    const labels = Object.keys(trend.demographics);
    const dataValues = Object.values(trend.demographics);

    pieChartRef.current = new ChartJS(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: dataValues,
            backgroundColor: CHART_COLORS.slice(0, 3),
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "65%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#8b5a2b",
              padding: 12,
              font: {
                family: "Inter",
                size: 11,
              },
            },
          },
          tooltip: { enabled: true },
        },
      },
    });

    return () => {
      if (pieChartRef.current) pieChartRef.current.destroy();
    };
  }, [trend.demographics]);

  const handleImageLoad = (i: number) => {
    setImagesLoaded((prev) => {
      const next = [...prev];
      next[i] = true;
      return next;
    });
  };

  return (
    <>
      <div className="box dashboard-box premium-card">
        {/* WGSN Premium Card Header */}
        <div className="premium-header">
          <div className="premium-header-left">
            <span className="premium-header-tag">Trend Forecast Report</span>
            <h2 className="premium-title">{trend.name}</h2>
            <span className="premium-subtitle">
              Pan India · Up to 2029 {cached && "· (cached)"}
            </span>
          </div>
          <div className="premium-header-right">
            <span className="premium-score-val">{trend.confidence}</span>
            <span className="premium-score-lbl">TREND SCORE</span>
          </div>
        </div>

        {/* WGSN Premium Card Body */}
        <div className="premium-body">
          {/* Tags / Badges Row */}
          <div className="premium-badges-row">
            <span className="premium-badge-momentum">{trend.momentum}</span>
            <span className="premium-badge-invest" style={{ backgroundColor: signalConfig.color }}>
              {trend.investSignal} — {investPercent}% budget
            </span>
          </div>

          {/* Trend Dynamic WGSN Report Description */}
          <p className="premium-trend-desc">{trend.description}</p>

          {/* Two-Column Trajectory & Details Layout */}
          <div className="premium-dashboard-grid">
            {/* Left Column: 3-Year Trajectory */}
            <div className="trajectory-column">
              <span className="trajectory-title">3-YEAR TRAJECTORY</span>
              <div className="trajectory-chart-container">
                <canvas ref={lineRef} id={`lineChart-${index}`}></canvas>
              </div>

              {/* Bar and Pie Charts added below the 3-Year Trajectory */}
              {(trend.graph || trend.demographics) && (
                <div className="charts-container">
                  {trend.graph && Object.keys(trend.graph).length > 0 && (
                    <div className="chart-wrapper">
                      <h3>Signal Strength</h3>
                      <canvas ref={barRef} id={`barChart-${index}`}></canvas>
                    </div>
                  )}
                  {trend.demographics && Object.keys(trend.demographics).length > 0 && (
                    <div className="chart-wrapper">
                      <h3>Demographics</h3>
                      <canvas ref={pieRef} id={`pieChart-${index}`}></canvas>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Right Column: WGSN Styled Details Stack */}
            <div className="details-column">
              {/* Box 1: Target Demographic */}
              {trend.targetDemographic && (
                <div className="detail-card">
                  <div className="detail-card-header">
                    <span className="detail-card-icon">🎯</span>
                    <span>Target demographic</span>
                  </div>
                  <div className="detail-card-text">{trend.targetDemographic}</div>
                </div>
              )}

              {/* Box 2: Peak Season */}
              {trend.peakSeason && (
                <div className="detail-card">
                  <div className="detail-card-header">
                    <span className="detail-card-icon">📅</span>
                    <span>Peak season</span>
                  </div>
                  <div className="detail-card-text">{trend.peakSeason}</div>
                </div>
              )}

              {/* Box 3: Competitor Activity */}
              {trend.competitorActivity && (
                <div className="detail-card">
                  <div className="detail-card-header">
                    <span className="detail-card-icon">🏷️</span>
                    <span>Competitor activity</span>
                  </div>
                  <div className="detail-card-text">{trend.competitorActivity}</div>
                </div>
              )}
            </div>
          </div>

          {/* Full-width Investment Advice Panel */}
          {trend.investReason && (
            <div className="premium-invest-panel">
              <span className="premium-invest-title">INVESTMENT ADVICE</span>
              <p className="premium-invest-reason">{trend.investReason}</p>
              {trend.risks && (
                <p className="premium-invest-risk">
                  ⚠️ {trend.risks.startsWith("Risk:") ? "" : "Risk: "}{trend.risks}
                </p>
              )}
            </div>
          )}

          {/* Style References Section */}
          {trend.images && trend.images.length > 0 && (
            <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginTop: "10px" }}>
              <span className="style-ref-header">STYLE REFERENCES</span>
              <div className="style-ref-row">
                {trend.images.slice(0, 3).map((src, i) => (
                  <div
                    key={i}
                    className="style-ref-card"
                    onClick={() => setLightboxSrc(src)}
                  >
                    {!imagesLoaded[i] && <div className="style-reference-skeleton" />}
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={src}
                      alt={`${trend.name} fashion reference ${i + 1}`}
                      className="style-ref-image"
                      style={{ opacity: imagesLoaded[i] ? 1 : 0 }}
                      onLoad={() => handleImageLoad(i)}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Inline lightbox for Unsplash images */}
      {lightboxSrc && (
        <div className="lightbox active" onClick={() => setLightboxSrc(null)}>
          <span className="lightbox-close" onClick={() => setLightboxSrc(null)}>×</span>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={lightboxSrc}
            alt="Expanded view"
            className="lightbox-img"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </>
  );
}
