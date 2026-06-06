import { useState, useEffect } from 'react';
import { Thermometer, Droplets, Wind, ShieldAlert, Scale, ClipboardCheck, CheckCircle, Search } from 'lucide-react';

// Telemetry Schema Definitions
interface SubsystemMetric {
  status?: string;
  risk_level?: string;
  message: string;
  feeding_multiplier?: number;
  cumulative_predicted_rainfall_mm?: number;
  action_required?: string;
}


interface WeatherInsights {
  meta: { location_name: string; latitude: number; longitude: number };
  atmospheric_snapshot: { temperature_c: number; precipitation_mm: number; humidity_percentage: number; wind_speed: number };
  aquaculture_insights: {
    thermal_management: SubsystemMetric;
    hydrology_safety: SubsystemMetric;
    dissolved_oxygen_risk: SubsystemMetric;
    feed_optimization: { recommended_feed_kg: number; adjustment_applied: string; feed_saved_g: number };
    action_plan: string[];
  };
}

export default function App() {
  // CONFIG FORM STATE MANAGEMENT
  const [latInput, setLatInput] = useState<string>("-0.42");
  const [lonInput, setLonInput] = useState<string>("36.95");
  const [feedInput, setFeedInput] = useState<string>("50.0");

  // RUNTIME APP TELEMETRY METRICS STATE
  const [telemetry, setTelemetry] = useState<WeatherInsights | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [checkedTasks, setCheckedTasks] = useState<Record<number, boolean>>({});

  // Asynchronous Fetch Request Routing Handler 
  const fetchTelemetryData = (lat: string, lon: string, baseFeed: string) => {
    setLoading(true);
    setError(null);
    setCheckedTasks({});

    fetch(`http://127.0.0.1:8000/api/weather?lat=${lat}&lon=${lon}&base_feed_kg=${baseFeed}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Data pipeline sync error. Status code: ${res.status}`);
        return res.json();
      })
      .then((data) => setTelemetry(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchTelemetryData(latInput, lonInput, feedInput);
  }, []);

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchTelemetryData(latInput, lonInput, feedInput);
  };

  if (loading && !telemetry) return <div style={{ padding: '48px', textAlign: 'center', color: '#64748b', fontWeight: 'bold' }}>Establishing Aqua-Shield Core Telemetry Link...</div>;
  if (error) return <div style={{ padding: '4px', color: '#b91c1c', textAlign: 'center', marginTop: '48px' }}>Sync Failure: {error}</div>;
  if (!telemetry) return null;

  const { atmospheric_snapshot: weather, aquaculture_insights: insights, meta } = telemetry;

  // Custom Semantic Status Style Router 
  const getBadgeStyle = (statusOrLevel?: string) => {
    const check = (statusOrLevel ?? '').toUpperCase();
    if (check === 'CRITICAL' || check === 'HIGH' || check === 'CRITICAL_LOW' || check === 'WARNING_HIGH') {
      return 'status-badge badge-rose';
    }
    if (check === 'MEDIUM' || check === 'WARNING_LOW' || check === 'UNKNOWN') {
      return 'status-badge badge-amber';
    }
    return 'status-badge badge-emerald';
  };

  return (
    <div className="dashboard-container">

      {/* APP HEADER */}
      <div className="app-header">
        <div>
          <span className="header-tag">Predictive Analytics Node</span>
          <h1>{meta.location_name}</h1>
          <p>GPS Grid Coordinates: {meta.latitude.toFixed(4)}°, {meta.longitude.toFixed(4)}°</p>
        </div>
        <div className="telemetry-status">
          {loading ? "🔄 Refreshing Channels..." : "● Telemetry Stream Active"}
        </div>
      </div>

      <label className="section-label">Insert New Telemetry Data , i.e. Location Coordinates (longitude, latitude) using two decimal places and Base Feed Ration (kg)</label>

      {/* CORE CONFIG FORM ROW */}
      <form onSubmit={handleFormSubmit} className="input-form">
        <div className="form-group">
          <label>Latitude</label>
          <input type="number" step="0.0001" value={latInput} onChange={(e) => setLatInput(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Longitude</label>
          <input type="number" step="0.0001" value={lonInput} onChange={(e) => setLonInput(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Base Feed Ration (kg)</label>
          <input type="number" step="0.1" value={feedInput} onChange={(e) => setFeedInput(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading} className="submit-btn">
          <Search size={14} /> Update Node Telemetry
        </button>
      </form>

      {/* CORE INFORMATION PANEL GRID */}
      <div className="main-grid">

        {/* COMPONENT MODULE READOUTS (LEFT SIDE) */}
        <div className="left-column">

          {/* WEATHER SNAPSHOT ROWS */}
          <div className="sensor-row">
            <div className="sensor-card">
              <div className="icon-wrapper bg-rose-light"><Thermometer size={18} /></div>
              <div>
                <p>Air Temp</p>
                <h3>{weather.temperature_c !== null && weather.temperature_c !== undefined ? `${weather.temperature_c}°C` : 'N/A'}</h3>
              </div>
            </div>
            <div className="sensor-card">
              <div className="icon-wrapper bg-blue-light"><Droplets size={18} /></div>
              <div>
                <p>Precipitation</p>
                <h3>{weather.precipitation_mm ?? 0} mm</h3>
              </div>
            </div>
            <div className="sensor-card">
              <div className="icon-wrapper bg-indigo-light"><Wind size={18} /></div>
              <div>
                <p>Wind Speed</p>
                <h3>{weather.wind_speed ?? 0} kph</h3>
              </div>
            </div>
            <div className="sensor-card">
              <div className="icon-wrapper bg-emerald-light"><ShieldAlert size={18} /></div>
              <div>
                <p>Humidity</p>
                <h3>{weather.humidity_percentage !== null && weather.humidity_percentage !== undefined ? `${weather.humidity_percentage}%` : 'N/A'}</h3>
              </div>
            </div>
          </div>

          {/* METABOLIC OPTIMIZATION CONTROLLER */}
          <div className="content-block">
            <div className="block-header">
              <div className="block-title-group">
                <Scale size={18} />
                <h2>Feed Optimization Counter</h2>
              </div>
              <span className={getBadgeStyle(insights.thermal_management.status)}>
                {insights.thermal_management.status ?? 'UNKNOWN'}
              </span>
            </div>

            <div className="feed-summary-box">
              <div className="feed-main-metric">
                <h4>Optimized Feeding Ration</h4>
                <div className="feed-large-text">{insights.feed_optimization.recommended_feed_kg} <span>kg</span></div>
                <div className="feed-sub-text">Scale Profile Factor: {insights.feed_optimization.adjustment_applied}</div>
              </div>
              <div>
                <h4 style={{ color: '#10b981' }}>✓ Inventory Saved</h4>
                <div className="feed-saved-text">{insights.feed_optimization.feed_saved_g} <span>g</span></div>
                <p className="feed-saved-desc">Preventing organic loading spikes to preserve water chemistry.</p>
              </div>
            </div>

            <div className="message-banner">
              {insights.thermal_management.message}
            </div>
          </div>

          {/* SECONDARY RISK CARDS */}
          <div className="risk-row">
            <div className="risk-card">
              <div className="risk-header-row">
                <span className="risk-label">Hydrology Safety</span>
                <span className={getBadgeStyle(insights.hydrology_safety.risk_level)}>{insights.hydrology_safety.risk_level}</span>
              </div>
              <p>{insights.hydrology_safety.action_required}</p>
              <div className="risk-extra-info">Predicted Cumulative Volume: {insights.hydrology_safety.cumulative_predicted_rainfall_mm} mm</div>
            </div>

            <div className="risk-card">
              <div className="risk-header-row">
                <span className="risk-label">Oxygen Stability</span>
                <span className={getBadgeStyle(insights.dissolved_oxygen_risk.risk_level)}>{insights.dissolved_oxygen_risk.risk_level}</span>
              </div>
              <p>{insights.dissolved_oxygen_risk.message}</p>
              <div className="risk-extra-info">Wind Stagnation Boundary: 5.0 kph</div>
            </div>
          </div>

        </div>

        {/* OPERATIONS TASK LIST ROUTER (RIGHT COLUMN) */}
        <div className="content-block">
          <div className="block-header" style={{ borderBottom: '1px solid #f1f5f9', paddingBottom: '12px', marginBottom: '0' }}>
            <div className="block-title-group">
              <ClipboardCheck size={16} style={{ color: '#4f46e5' }} />
              <h2>Operational Task Routing</h2>
            </div>
          </div>

          <div className="task-list">
            {insights.action_plan.map((task, idx) => {
              const isDone = !!checkedTasks[idx];
              return (
                <div
                  key={idx}
                  onClick={() => setCheckedTasks(prev => ({ ...prev, [idx]: !prev[idx] }))}
                  className={`task-item ${isDone ? 'completed' : ''}`}
                >
                  {isDone ? <CheckCircle size={15} style={{ color: '#10b981', flexShrink: 0, marginTop: '2px' }} /> : <div className="checkbox-mock" />}
                  <span>{task}</span>
                </div>
              );
            })}
          </div>
        </div>

      </div>
    </div>
  );
}