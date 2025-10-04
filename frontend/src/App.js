import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import axios from 'axios';
import { format } from 'date-fns';
import './index.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

function MapClickHandler({ onLocationSelect }) {
  useMapEvents({
    click: (e) => {
      onLocationSelect({
        latitude: e.latlng.lat,
        longitude: e.latlng.lng
      });
    },
  });
  return null;
}

function App() {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Set default dates (last 30 days)
  React.useEffect(() => {
    const today = new Date();
    const thirtyDaysAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);
    
    setEndDate(format(today, 'yyyy-MM-dd'));
    setStartDate(format(thirtyDaysAgo, 'yyyy-MM-dd'));
  }, []);

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedLocation) {
      setError('Please select a location on the map');
      return;
    }

    if (!startDate || !endDate) {
      setError('Please select both start and end dates');
      return;
    }

    if (new Date(startDate) >= new Date(endDate)) {
      setError('Start date must be before end date');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('/analysis/', {
        location: {
          latitude: selectedLocation.latitude,
          longitude: selectedLocation.longitude
        },
        date_range: {
          start_date: startDate,
          end_date: endDate
        }
      });

      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while analyzing climate data');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🌍 Skyluxe</h1>
        <p>Climate Analysis Platform - Click on the map to select a location</p>
      </header>

      <div className="analysis-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="map">Select Location:</label>
            <div className="map-container">
              <MapContainer
                center={[40.7128, -74.0060]}
                zoom={10}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                <MapClickHandler onLocationSelect={handleLocationSelect} />
                {selectedLocation && (
                  <Marker position={[selectedLocation.latitude, selectedLocation.longitude]} />
                )}
              </MapContainer>
            </div>
            {selectedLocation && (
              <div className="location-display">
                <strong>Selected Location:</strong> {selectedLocation.latitude.toFixed(4)}, {selectedLocation.longitude.toFixed(4)}
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Date Range:</label>
            <div className="date-inputs">
              <div>
                <label htmlFor="startDate">Start Date:</label>
                <input
                  type="date"
                  id="startDate"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  max={endDate}
                />
              </div>
              <div>
                <label htmlFor="endDate">End Date:</label>
                <input
                  type="date"
                  id="endDate"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  min={startDate}
                />
              </div>
            </div>
          </div>

          {error && <div className="error">{error}</div>}

          <button
            type="submit"
            className="submit-button"
            disabled={isLoading || !selectedLocation}
          >
            {isLoading ? 'Analyzing Climate Data...' : 'Analyze Climate'}
          </button>
        </form>
      </div>

      {isLoading && (
        <div className="loading">
          <h2>🔄 Analyzing Climate Data...</h2>
          <p>This may take a few moments while we fetch weather data from NASA POWER API.</p>
        </div>
      )}

      {results && (
        <div className="results">
          <h2>📊 Climate Analysis Results</h2>
          <div className="success">
            Analysis completed successfully for {results.data_summary.total_days} days of data.
          </div>
          
          <h3>Location & Date Range</h3>
          <p>
            <strong>Location:</strong> {results.location.latitude.toFixed(4)}, {results.location.longitude.toFixed(4)}<br/>
            <strong>Period:</strong> {results.data_summary.date_range.start} to {results.data_summary.date_range.end}
          </p>

          <h3>Analysis Results</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
